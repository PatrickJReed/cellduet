"""Tahoe-100M streaming loader and per-drug aggregation helpers.

The full Tahoe expression atlas is 337 GB on Hugging Face; this module
streams the `pseudobulk_differential_expression` config and aggregates
to per-(drug, cell_line) log-fold-change vectors. See
docs/datasets/tahoe-100m.md for distribution and license details.
"""
from typing import Iterable, List, Optional

import pandas as pd


def plate_match_dmso(
    df: pd.DataFrame,
    dmso_label: str = "DMSO_TF",
    plate_col: str = "plate",
    drug_col: str = "drug",
) -> pd.DataFrame:
    """Drop drug rows on plates that have no DMSO control row, and drop DMSO rows.

    Tahoe pairs (drug, plate) against (DMSO_TF, plate) for the LFC contrast.
    This function enforces that a drug row's plate must also carry DMSO_TF, and
    returns only the non-DMSO rows ready for downstream aggregation.
    """
    plates_with_dmso = set(df.loc[df[drug_col] == dmso_label, plate_col].unique())
    return df[(df[drug_col] != dmso_label) & (df[plate_col].isin(plates_with_dmso))].copy()


def aggregate_per_drug(
    df: pd.DataFrame,
    value_cols: Iterable[str],
    group_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Mean-aggregate value_cols across replicate rows within each group.

    Default group is (drug, cell_line). Returns a dataframe indexed by the
    grouping columns with one column per value_col.
    """
    if group_cols is None:
        group_cols = ["drug", "cell_line"]
    return df.groupby(list(group_cols))[list(value_cols)].mean()


def stream_pseudobulk_de_to_tall_df(
    repo_id: str = "tahoebio/Tahoe-100M",
    config: str = "pseudobulk_differential_expression",
    drugs_filter: Optional[Iterable[str]] = None,
    genes_filter: Optional[Iterable[str]] = None,
    batch_size: int = 50_000,
    drug_col: str = "drug",
    gene_col: str = "gene_symbol",
) -> pd.DataFrame:
    """Stream Tahoe's pre-computed pseudobulk DE table from HF, optionally filtered.

    Returns a tall pandas dataframe whose schema is set by the dataset's columns.
    Use drugs_filter and genes_filter to keep memory bounded.

    Note: column names in the parquet should be confirmed empirically in
    notebook 02 before this function is called. Adjust drug_col / gene_col
    if the schema differs.
    """
    from datasets import load_dataset  # imported lazily so unit tests don't require it

    ds = load_dataset(repo_id, config, streaming=True, split="train")
    chunks: List[pd.DataFrame] = []
    drugs_set = set(drugs_filter) if drugs_filter is not None else None
    genes_set = set(genes_filter) if genes_filter is not None else None
    for batch in ds.iter(batch_size=batch_size):
        sub = pd.DataFrame(batch)
        if drugs_set is not None and drug_col in sub.columns:
            sub = sub[sub[drug_col].isin(drugs_set)]
        if genes_set is not None and gene_col in sub.columns:
            sub = sub[sub[gene_col].isin(genes_set)]
        if not sub.empty:
            chunks.append(sub)
    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()
