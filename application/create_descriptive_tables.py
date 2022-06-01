from pathlib import Path

import numpy as np
import pandas as pd
import scikits.bootstrap
from dfmvis.data_loaders import load_dfm
from wasabi import msg


def generate_prop_by_source_by_cat_table(dfm, output_filename, col_prefix, bootstrap = True):
    cols_with_prefix = [col for col in dfm if col.startswith(col_prefix)]
    cols_to_keep = cols_with_prefix + ["tokens", "source"]
    
    cols_for_total = [col for col in cols_to_keep if col not in ("source", "tokens")]

    dfm = dfm[cols_to_keep]

    dfm_document_counts = dfm[["source"]]
    dfm_document_counts["Docs"] = 1
    dfm_document_counts = dfm_document_counts.groupby("source").sum()

    dfm[f"Mean count from all {col_prefix}"] = dfm[cols_for_total].sum(axis=1)

    # Add proportions
    cols_to_convert_to_prop = cols_with_prefix + [f"Mean count from all {col_prefix}"]
    prefix_length = len(col_prefix)

    dfm = add_count_as_proportion_of_all_tokens_columns(prefix_length, dfm, cols_to_convert_to_prop)
    cat_by_source = dfm

    # Rename cols with prefix
    for old_col_name in cols_with_prefix:
        category_name = old_col_name[prefix_length + 1 :]
        new_col_name = f"Mean {category_name} token count"

        cat_by_source[new_col_name] = round(
            cat_by_source[old_col_name], 4
        )
        cat_by_source.drop(old_col_name, axis = 1, inplace=True)

    # Bootstrapping
    cols_to_bootstrap = [col for col in cat_by_source.columns.tolist() if col not in ["source"]]
    aggregated = dfm.groupby("source").mean()

    if bootstrap:
        grouped = dfm.groupby("source")
        n_cols = len(cols_to_bootstrap)

        for i, col in enumerate(cols_to_bootstrap):
            msg.info(f"{i} / {n_cols}: Bootstrapping '{col}'")

            # Documentation for bootstraps: https://necromuralist.github.io/boston_housing/api/scikits.bootstrap.ci.html
            cis = grouped[col].apply(lambda x: scikits.bootstrap.ci(data=x, n_samples=1000))
            aggregated[f"{col}_ci"] = cis
    
    aggregated["Docs"] = dfm_document_counts

    output_path = Path(__file__).parent.parent / "tables" / f"{output_filename}"
    aggregated.reset_index().to_csv(output_path)

def add_count_as_proportion_of_all_tokens_columns(prefix_length, cat_by_source, cols_to_convert_to_prop):
    for old_col_name in cols_to_convert_to_prop:
        category_name = old_col_name[prefix_length + 1 :]
        new_col_name = f"Mean {category_name} (%)"

        cat_by_source[new_col_name] = round(
            cat_by_source[old_col_name] / cat_by_source["tokens"] * 100, 4
        )
        
    return cat_by_source


if __name__ == "__main__":
    csv_dir = Path(__file__).parent.parent / "data" / "shaped"

    categories = {
        "religion": {
            "col_prefix": "rel",
        },
        "gender": {"col_prefix": "gender"},
    }

    dfm = load_dfm()

    for outcome, info in categories.items():
        file_name = f"{outcome}_by_source_wide.csv"

        generate_prop_by_source_by_cat_table(
            dfm=dfm,
            col_prefix=info["col_prefix"],
            output_filename=f"{outcome}_table.csv",
        )
