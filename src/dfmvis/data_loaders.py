from pathlib import Path
from time import time
from typing import List

import pandas as pd
from wasabi import Printer


def load_dataset(filename: str) -> pd.DataFrame:
    msg = Printer(timestamp=True)

    msg.info(f"Loading {filename}")
    project_dir = Path(__file__).parent.parent.parent
    file_path = project_dir / "data" / "unshaped" / filename
    raw_data = pd.read_csv(file_path, nrows=50_000)

    if "text" in raw_data.columns:
        return raw_data.drop(["text"], axis=1)
    else:
        return raw_data


def load_dagw() -> pd.DataFrame:
    return load_dataset("dagw_dfm_counts.csv")


def load_danews() -> pd.DataFrame:
    return load_dataset("danews_counts.csv")


def load_hopetwitter() -> pd.DataFrame:
    return load_dataset("hopetwitter_counts.csv")


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
