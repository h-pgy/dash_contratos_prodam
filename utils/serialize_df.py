from config import DATA_PATH
import os
import pandas as pd


def solve_fpath(fname:str, folder:str=DATA_PATH)->str:

    if not os.path.exists(folder):
        os.mkdir(folder)
        folder = os.path.abspath(folder)

    return os.path.join(folder, fname)

def df_to_parquet(df, fname: str, folder=DATA_PATH) -> str:

    if not fname.endswith('.parquet'):
        raise ValueError(f'File must be .parquet')
    
    fpath: str = solve_fpath(fname, folder)

    df.to_parquet(fpath, index=False)

    return fpath


def read_parquet_df(fname:str, folder:str=DATA_PATH)->pd.DataFrame:

    if not fname.endswith('.parquet'):
        raise ValueError(f'File must be .parquet')
    
    fpath: str = solve_fpath(fname, folder)

    return pd.read_parquet(fpath)