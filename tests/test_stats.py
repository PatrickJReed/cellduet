"""Tests for src/cellduet/stats.py."""

import numpy as np
import pytest
from scipy.spatial.distance import pdist, squareform

from cellduet.stats import (
    mantel,
    neighborhood_jaccard,
    permutation_null,
    rv_coefficient,
)


def _two_random_distance_matrices(n=50, seed=0):
    rng = np.random.default_rng(seed)
    X1 = rng.normal(size=(n, 16))
    X2 = rng.normal(size=(n, 16))
    return squareform(pdist(X1, metric="cosine")), squareform(pdist(X2, metric="cosine"))


def _correlated_distance_matrices(n=50, noise=0.1, seed=0):
    """Build two distance matrices that share underlying structure."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 16))
    X1 = X + rng.normal(size=X.shape, scale=noise)
    X2 = X + rng.normal(size=X.shape, scale=noise)
    return squareform(pdist(X1, metric="cosine")), squareform(pdist(X2, metric="cosine"))


def test_mantel_self_correlation_is_one():
    D, _ = _two_random_distance_matrices()
    r, _ = mantel(D, D, n_permutations=0)
    assert r == pytest.approx(1.0)


def test_mantel_random_pair_low_correlation():
    D1, D2 = _two_random_distance_matrices(n=100)
    r, p = mantel(D1, D2, n_permutations=999)
    assert -0.3 < r < 0.3
    assert p > 0.01


def test_mantel_correlated_pair_significant_correlation():
    D1, D2 = _correlated_distance_matrices(n=80, noise=0.05)
    r, p = mantel(D1, D2, n_permutations=999)
    assert r > 0.5
    assert p < 0.01


def test_mantel_zero_permutations_returns_nan_p():
    D1, D2 = _two_random_distance_matrices()
    r, p = mantel(D1, D2, n_permutations=0)
    assert not np.isnan(r)
    assert np.isnan(p)


def test_mantel_shape_mismatch_raises():
    D1, _ = _two_random_distance_matrices(n=10)
    D2, _ = _two_random_distance_matrices(n=20)
    with pytest.raises(ValueError):
        mantel(D1, D2, n_permutations=0)


def test_rv_coefficient_in_unit_range():
    D1, D2 = _two_random_distance_matrices()
    rv = rv_coefficient(D1, D2)
    assert 0.0 <= rv <= 1.0


def test_rv_coefficient_self_is_one():
    D, _ = _two_random_distance_matrices()
    assert rv_coefficient(D, D) == pytest.approx(1.0)


def test_neighborhood_jaccard_self_is_one():
    D, _ = _two_random_distance_matrices()
    j = neighborhood_jaccard(D, D, k=5)
    assert all(v == 1.0 for v in j)


def test_neighborhood_jaccard_returns_per_row_array():
    D1, D2 = _two_random_distance_matrices(n=30)
    j = neighborhood_jaccard(D1, D2, k=5)
    assert j.shape == (30,)
    assert all(0.0 <= v <= 1.0 for v in j)


def test_permutation_null_returns_distribution():
    D1, D2 = _two_random_distance_matrices(n=50)
    null_dist = permutation_null(D1, D2, statistic=mantel, n_permutations=100)
    assert len(null_dist) == 100
    # Random permutations should produce a roughly mean-zero distribution
    assert abs(null_dist.mean()) < 0.1
