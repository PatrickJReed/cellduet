"""CPJUMP1 (cpg0000-jump-pilot) loader for the A549 sanity-check arm.

CPJUMP1 ships per-plate CellProfiler features at multiple processing
stages. Per-plate feature selection means the column schema can vary
across plates within a single batch; this module provides the alignment
step that intersects feature columns before per-compound aggregation.
See docs/datasets/cpjump1.md.
"""

from collections.abc import Sequence

import pandas as pd


def align_per_plate_features(plate_dfs: Sequence[pd.DataFrame]) -> pd.DataFrame:
    """Concatenate per-plate feature dataframes, keeping only common columns.

    Parameters
    ----------
    plate_dfs : sequence of dataframes
        One dataframe per plate. Each may have a different set of columns.

    Returns
    -------
    DataFrame
        Concatenation of all plate frames, restricted to the column-set
        intersection across plates. Row order within each plate is preserved.
    """
    if not plate_dfs:
        return pd.DataFrame()
    common = set(plate_dfs[0].columns)
    for df in plate_dfs[1:]:
        common &= set(df.columns)
    common_cols = [c for c in plate_dfs[0].columns if c in common]
    return pd.concat([df[common_cols] for df in plate_dfs], ignore_index=True)
