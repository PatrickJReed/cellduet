"""JUMP-CP cpg0016 loader and per-compound aggregation.

The harmony-corrected feature parquet for cpg0016 is at
s3://cellpainting-gallery/cpg0016-jump-assembled/profiles/COMPOUND/v1.0/
profiles_var_mad_int_featselect_harmony.parquet (~2.64 GB, CC0-1.0).
This module provides the per-compound aggregation step; loaders and S3
fetch belong in the notebook so they can be inspected interactively.
See docs/datasets/jump-cp-cpg0016.md.
"""

from collections.abc import Iterable

import pandas as pd


def aggregate_per_compound(
    df: pd.DataFrame,
    feature_cols: Iterable[str],
    compound_col: str = "inchikey",
) -> pd.DataFrame:
    """Mean-aggregate feature columns across replicate wells per compound.

    Returns a dataframe indexed by compound_col with one column per feature.
    """
    return df.groupby(compound_col)[list(feature_cols)].mean()
