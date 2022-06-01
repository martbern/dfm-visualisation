import pandas as pd

from create_shaped_datasets import co_occurrence


def str_to_df(str) -> pd.DataFrame:
    from io import StringIO

    df = pd.read_table(StringIO(str), sep=",", index_col=False)

    # Drop "Unnamed" cols
    return df.loc[:, ~df.columns.str.contains("^Unnamed")]


def test_cooccurence():
    input_str = """porn1,porn2,porn3,porn4
                            1,1,2,0
                            0,0,2,0
                            """

    input_df = str_to_df(input_str)
    porn_cols = ["porn1", "porn2", "porn3", "porn4"]

    df = co_occurrence(input_df, porn_cols, round_if_fewer_than_n_cols=2, round_to=0)

    assert df.iloc[0].sum() == 4
    assert df.iloc[1].sum() == 0
