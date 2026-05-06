"""Tests for src/cellduet/jump.py."""

import pandas as pd
import pytest

from cellduet.jump import aggregate_per_compound


def test_aggregate_per_compound_means_replicates():
    df = pd.DataFrame(
        {
            "inchikey": ["X", "X", "X", "Y", "Y"],
            "feat_a": [1.0, 2.0, 3.0, 10.0, 12.0],
            "feat_b": [0.0, 1.0, 2.0, -1.0, 1.0],
        }
    )
    result = aggregate_per_compound(df, feature_cols=["feat_a", "feat_b"], compound_col="inchikey")
    assert result.loc["X", "feat_a"] == pytest.approx(2.0)
    assert result.loc["X", "feat_b"] == pytest.approx(1.0)
    assert result.loc["Y", "feat_a"] == pytest.approx(11.0)


def test_aggregate_per_compound_supports_alternate_compound_col():
    df = pd.DataFrame(
        {
            "broad_sample": ["a", "a", "b"],
            "feat_a": [1.0, 3.0, 5.0],
        }
    )
    result = aggregate_per_compound(df, feature_cols=["feat_a"], compound_col="broad_sample")
    assert result.loc["a", "feat_a"] == pytest.approx(2.0)
    assert result.loc["b", "feat_a"] == pytest.approx(5.0)
