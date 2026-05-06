"""Tests for src/cellduet/tahoe.py."""

import pandas as pd
import pytest

from cellduet.tahoe import aggregate_per_drug, plate_match_dmso


def test_plate_match_dmso_drops_unmatched_plates():
    # Two drug rows on plate A, one DMSO row on plate B; drug rows must drop
    df = pd.DataFrame(
        {
            "sample": ["s1", "s2", "s3"],
            "drug": ["DrugX", "DrugX", "DMSO_TF"],
            "plate": ["A", "A", "B"],
            "log_fold_change": [1.0, 1.5, 0.0],
        }
    )
    result = plate_match_dmso(df)
    assert len(result) == 0


def test_plate_match_dmso_keeps_matched_plates():
    df = pd.DataFrame(
        {
            "sample": ["s1", "s2", "s3"],
            "drug": ["DrugX", "DMSO_TF", "DrugY"],
            "plate": ["A", "A", "A"],
            "log_fold_change": [1.0, 0.0, 2.0],
        }
    )
    result = plate_match_dmso(df)
    assert set(result["drug"]) == {"DrugX", "DrugY"}


def test_plate_match_dmso_drops_dmso_rows():
    df = pd.DataFrame(
        {
            "sample": ["s1", "s2", "s3"],
            "drug": ["DrugX", "DMSO_TF", "DMSO_TF"],
            "plate": ["A", "A", "A"],
            "log_fold_change": [1.0, 0.0, 0.0],
        }
    )
    result = plate_match_dmso(df)
    assert "DMSO_TF" not in set(result["drug"])
    assert set(result["drug"]) == {"DrugX"}


def test_aggregate_per_drug_means_across_gemgroups():
    df = pd.DataFrame(
        {
            "drug": ["X", "X", "Y"],
            "cell_line": ["A549", "A549", "A549"],
            "gemgroup": ["g1", "g2", "g1"],
            "gene_X": [1.0, 3.0, 5.0],
            "gene_Y": [2.0, 4.0, 6.0],
        }
    )
    result = aggregate_per_drug(df, value_cols=["gene_X", "gene_Y"])
    assert result.loc[("X", "A549"), "gene_X"] == pytest.approx(2.0)
    assert result.loc[("X", "A549"), "gene_Y"] == pytest.approx(3.0)
    assert result.loc[("Y", "A549"), "gene_X"] == pytest.approx(5.0)


def test_aggregate_per_drug_supports_custom_group_cols():
    df = pd.DataFrame(
        {
            "drug": ["X", "X"],
            "cell_line": ["A549", "MCF7"],
            "gene_X": [1.0, 9.0],
        }
    )
    result = aggregate_per_drug(df, value_cols=["gene_X"], group_cols=["drug"])
    assert result.loc["X", "gene_X"] == pytest.approx(5.0)
