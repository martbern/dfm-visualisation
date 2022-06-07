from pathlib import Path
from typing import List

import pandas as pd
from wasabi import Printer


def create_duplicates_column(df, columns_for_detection, duplicates_colname = "duplicate"):
    df["duplicate"] = df.duplicated(subset=columns_for_detection, keep="first")
    return df


def load_dataset(filename: str, drop_text: bool = True, drop_duplicates: bool = True, drop_na: bool = True) -> pd.DataFrame:
    msg = Printer(timestamp=True)

    msg.info(f"Loading {filename}")
    project_dir = Path(__file__).parent.parent.parent
    file_path = project_dir / "data" / "unshaped" / filename
    df = pd.read_csv(file_path)

    if drop_duplicates:
        df = create_duplicates_column(df, columns_for_detection=df.columns)

        n_duplicates = df["duplicate"].sum()
        duplicate_percent = round(n_duplicates / df.shape[0], 2)

        msg.warn(f"Dropping {n_duplicates} ({duplicate_percent}%) duplicates from {filename}")

        # Drop all rows where "duplicate" column is 1
        df = df[df["duplicate"] == False]

    if drop_na:
        rows_with_na = df[df.isna().any(axis=1)]
        n_rows_with_na = rows_with_na.shape[0]

        if n_rows_with_na > 0:
            msg.warn(f"Dropping {n_rows_with_na} rows with NAs")
            df = df[df.isna().any(axis=1) == False]

    if drop_text:
        if "text" in df.columns:
            df = df.drop(["text"], axis=1)

    return df


def load_dagw() -> pd.DataFrame:
    return load_dataset("dagw_dfm_counts.csv")


def load_danews() -> pd.DataFrame:
    return load_dataset("danews_counts.csv")


def load_hopetwitter(drop_text = True) -> pd.DataFrame:
    return load_dataset("hopetwitter_counts.csv", drop_text=drop_text)


def load_nat() -> pd.DataFrame:
    return load_dataset("nat_counts.csv")


def load_dfm() -> List[pd.DataFrame]:
    sources = {
        "Danish Gigaword": load_dagw,
        "DaNews": load_danews,
        "HopeTwitter": load_hopetwitter,
        "NAT": load_nat,
    }

    named_datasets = []

    for name, loader in sources.items():
        df = loader()

        df["source"] = name
        named_datasets.append(df)

    return pd.concat(named_datasets, axis=0).reset_index()
