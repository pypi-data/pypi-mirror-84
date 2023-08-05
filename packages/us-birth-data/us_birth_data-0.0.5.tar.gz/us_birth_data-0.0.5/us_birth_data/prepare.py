import gzip
import shutil
import subprocess
from ftplib import FTP
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from tqdm import tqdm

from us_birth_data import fields
from us_birth_data.files import YearData

gzip_path = Path('gz')


class FtpGet:
    """ Context manager class to handle the download of data set archives and documentation """
    host = 'ftp.cdc.gov'
    data_set_path = '/pub/Health_Statistics/NCHS/Datasets/DVS/natality'

    def __init__(self):
        self.ftp = FTP(self.host)
        self.ftp.login()

    def __enter__(self):
        self.ftp.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ftp.close()

    def get_file(self, file_name, destination: Path):
        p = Path(destination, file_name)
        total = self.ftp.size(file_name)

        print(f"Starting download of {file_name}")
        with p.open('wb') as f:
            with tqdm(total=total) as progress_bar:
                def cb(chunk):
                    data_length = len(chunk)
                    progress_bar.update(data_length)
                    f.write(chunk)

                self.ftp.retrbinary(f'RETR {file_name}', cb)
        return p

    def list_data_sets(self):
        self.ftp.cwd(self.data_set_path)
        return self.ftp.nlst()

    def get_data_set(self, file_name, destination: Path):
        self.ftp.cwd(self.data_set_path)
        self.get_file(file_name, destination)


def zip_convert(zip_file):
    """
    Unzip file, recompress pub file as gz

    Requires 7zip to be installed so that it can be called as `7z` by a subprocess.

    Note: we can't use the built-in unzip package in python as some of the files
    we need to inflate are compressed using algorithms which python is not licensed
    to use.
    """
    print(f"Convert to gzip: {zip_file}")
    with TemporaryDirectory() as td:
        subprocess.check_output(['7z', 'x', zip_file, '-o' + Path(td).as_posix()])

        sizes = [(fp.stat().st_size, fp) for fp in Path(td).rglob('*') if fp.is_file()]
        sizes.sort(reverse=True)

        with sizes[0][1].open('rb') as f_in:  # assume largest file is actual data
            with gzip.open(Path(gzip_path, zip_file.stem + sizes[0][1].suffix + '.gz'), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    zip_file.unlink()


def stage_gzip(file_name):
    with TemporaryDirectory() as td:
        with FtpGet() as ftp:
            file_path = Path(td, file_name)
            ftp.get_data_set(file_name, file_path.parent)
        zip_convert(file_path)


def get_queue():
    queue = []
    with FtpGet() as ftp:
        available = ftp.list_data_sets()

    existing = [x.stem for x in gzip_path.iterdir() if x.is_file()]
    for data_set in available:
        if not any([x.startswith(Path(data_set).stem) for x in existing]):
            queue.append(data_set)
    return queue


def reduce(year_from=1968, year_to=9999, sample_size=0):
    tc = {x.name(): x.pd_type for x in fields.targets}
    mdf = pd.DataFrame()

    for file in YearData.__subclasses__():
        if year_from <= file.year <= year_to:

            print(f"Counting rows in {file.pub_file}")
            if sample_size:
                total = sample_size
            else:
                with gzip.open(Path(gzip_path, file.pub_file), 'rb') as r:
                    total = sum(1 for _ in r)
            print(f"{total} rows")

            fd = {x: [] for x in fields.sources}
            print(f"Extracting raw data from {file.pub_file}")
            with gzip.open(Path(gzip_path, file.pub_file), 'rb') as r:
                for ix, line in enumerate(tqdm(r, total=total)):
                    if sample_size and ix > sample_size:
                        break
                    if not line.isspace():
                        for k, v in fd.items():
                            fd[k].append(k.parse_from_row(file, line))

            new_keys = [x.name() for x in fd.keys()]
            fd = dict(zip(new_keys, fd.values()))
            df = pd.DataFrame.from_dict(fd)

            kw = dict(year=file.year)
            print(f"Reshaping {str(file.year)} data")
            for t in fields.targets:
                df[t.name()] = t.remap(df, **kw)

            df = df[list(tc.keys())]
            print(f"Grouping {str(file.year)} data")
            df = df.groupby(
                [x for x in df.columns.tolist() if x != fields.Births.name()],
                as_index=False, dropna=False
            )[fields.Births.name()].sum()

            mdf = df if df.empty else pd.concat([mdf, df])

    mdf = mdf.astype(tc)
    return mdf


def generate_parquet():
    gzip_path.mkdir(exist_ok=True)
    for q in get_queue():
        stage_gzip(q)

    reduce().to_parquet(
        Path(Path(__file__).parent, 'us_birth_data.parquet')
    )
