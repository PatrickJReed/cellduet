"""Tests for src/cellduet/cpjump1.py."""
import pandas as pd

from cellduet.cpjump1 import align_per_plate_features


def test_align_intersects_columns():
    p1 = pd.DataFrame({"a": [1, 2], "b": [3, 4], "extra1": [9, 9]})
    p2 = pd.DataFrame({"a": [5, 6], "b": [7, 8], "extra2": [9, 9]})
    out = align_per_plate_features([p1, p2])
    assert set(out.columns) == {"a", "b"}
    assert len(out) == 4


def test_align_preserves_row_order_within_plate():
    p1 = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
    p2 = pd.DataFrame({"a": [4, 5], "b": [40, 50]})
    out = align_per_plate_features([p1, p2])
    assert out["a"].tolist() == [1, 2, 3, 4, 5]
    assert out["b"].tolist() == [10, 20, 30, 40, 50]


def test_align_single_plate_passes_through():
    p1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    out = align_per_plate_features([p1])
    assert set(out.columns) == {"a", "b"}
    assert len(out) == 2
