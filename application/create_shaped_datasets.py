from pathlib import Path

import numpy as np
import pandas as pd
from dfmvis.data_loaders import load_dfm
from wasabi import Printer


def write_gender_pronoun_by_source_csv(
    dfm: pd.DataFrame,
    without_0,
    csv_dir: Path,
    direction: str,
    wide_cols=["positive_words", "negative_words", "source", "tokens", "porn_prop"],
):
    """_summary_

    Args:
        dfm (pd.DataFrame): _description_
        without_0 (_type_): Whether to drop all documents that don't contain any
            gender pronouns.
    """
    ds = dfm

    genders = ["male", "female"]
    gender_count_cols = []
    gender_prop_cols = []

    for gender in genders:
        gender_counts = ds[f"gender_{gender}_pronoun"]

        new_prop_col_name = f"prop_pronoun_{gender}"
        ds[new_prop_col_name] = gender_counts / ds["tokens"]
        gender_prop_cols.append(new_prop_col_name)

        new_count_col_name = f"pronoun_{gender}"
        ds[new_count_col_name] = gender_counts
        gender_count_cols.append(new_count_col_name)

    ds["row_num"] = np.arange(ds.shape[0])

    filename = f"pronoun_by_source_{direction}"

    if without_0 == True:
        ds["gender_pronoun_tokens"] = ds[gender_count_cols].sum(axis=1)
        ds = ds[ds["gender_pronoun_tokens"] > 0]
        filename = filename + "_without_0"

    if direction == "long":
        stubs = ["prop_pronoun", "pronoun"]
        ds = pd.wide_to_long(
            ds,
            stubnames=stubs,
            i=["row_num", "source"],
            j="gender",
            sep="_",
            suffix=r"\D+",
        ).reset_index()
        ds[stubs + ["gender", "source"]].to_csv(str(csv_dir) + "/" + filename + ".csv")
    elif direction == "wide":
        ds[gender_count_cols + gender_prop_cols + wide_cols].to_csv(
            str(csv_dir) + "/" + filename + ".csv"
        )
    else:
        raise ValueError("Shape must be either long or wide")


def write_religion_by_source_csv(
    dfm: pd.DataFrame,
    without_0,
    csv_dir: Path,
    direction: str,
    wide_cols=["positive_words", "negative_words", "source", "tokens", "porn_prop"],
):
    """_summary_

    Args:
        dfm (pd.DataFrame): _description_
        without_0 (_type_): Whether to drop all documents that don't contain any
            gender pronouns.
    """
    ds = dfm

    religions = ["muslim", "christian", "jew", "buddhist", "hindu", "atheist"]

    religion_count_cols = []
    religion_prop_cols = []

    for religion in religions:
        prop_colname = f"prop_{religion}"
        ds[prop_colname] = ds[f"rel_{religion}"] / ds["tokens"]

        religion_count_cols.append(f"rel_{religion}")
        religion_prop_cols.append(prop_colname)

    ds = ds[religion_count_cols + religion_prop_cols + wide_cols]
    ds["row_num"] = np.arange(ds.shape[0])
    filename = f"religion_by_source_{direction}"

    if without_0 == True:
        ds["rel_tokens"] = ds[religion_count_cols].sum(axis=1)
        ds = ds[ds["rel_tokens"] > 0]
        filename += "_without_0"

    if direction == "long":
        ds = pd.wide_to_long(
            ds,
            stubnames=["rel", "prop"],
            i=["row_num", "source"],
            j="religion",
            sep="_",
            suffix=r"\D+",
        ).reset_index()
        ds[["rel", "prop", "religion", "source"]].to_csv(
            str(csv_dir) + "/" + filename + ".csv"
        )
    elif direction == "wide":
        ds[religion_count_cols + religion_prop_cols + wide_cols].to_csv(
            str(csv_dir) + "/" + filename + ".csv"
        )
    else:
        raise ValueError("Shape must be either long or wide")


def co_occurrence(df, porn_cols, round_if_fewer_than_n_cols, round_to):
    df["n_cols_represented"] = df[df[porn_cols] > 0].count(axis=1)
    df[porn_cols] = df[porn_cols].mask(
        df["n_cols_represented"] < round_if_fewer_than_n_cols, round_to
    )

    return df.drop("n_cols_represented", axis=1)


if __name__ == "__main__":
    msg = Printer(timestamp=True)

    msg.info("Loading dfm")
    dfm = load_dfm()

    csv_dir = Path(__file__).parent.parent / "data" / "shaped"

    dfm.to_csv(csv_dir / "dfm.csv")

    msg.good("Finished loading dfm")

    porn_cols = [col for col in dfm.columns if col.startswith("porn_")]
    biased_porn = [f"porn_{term}" for term in ["kvinder", "piger", "damer", "fanden"]]

    for biased_col in biased_porn:
        porn_cols.remove(biased_col)

    dfm["prop_porn"] = dfm[porn_cols].sum(axis=1) / dfm["tokens"]

    msg.info("Handling co-occurrence in porn")
    dfm = co_occurrence(dfm, porn_cols, round_if_fewer_than_n_cols=4, round_to=0)

    # Handle affect
    msg.info("Handling affect")
    for affect in ["positive", "negative"]:
        dfm[f"prop_{affect}"] = dfm[f"{affect}_words"] / dfm["tokens"]

    wide_cols = [
        "prop_positive",
        "prop_negative",
        "negative_words",
        "source",
        "tokens",
        "prop_porn",
    ]

    for without_0 in [True, False]:
        for direction in ["long", "wide"]:
            msg.info(f"Writing {direction} with without_0 = {without_0}")

            write_gender_pronoun_by_source_csv(
                dfm,
                without_0=without_0,
                csv_dir=csv_dir,
                direction=direction,
                wide_cols=wide_cols,
            )
            write_religion_by_source_csv(
                dfm,
                without_0=without_0,
                csv_dir=csv_dir,
                direction=direction,
                wide_cols=wide_cols,
            )
