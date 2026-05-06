"""Tests for src/cellduet/rxrx3.py."""

import numpy as np

from cellduet.rxrx3 import typical_variation_normalization


def test_tvn_zeros_mean_on_controls():
    rng = np.random.default_rng(42)
    n_wells, n_dims = 200, 16
    is_control = np.zeros(n_wells, dtype=bool)
    is_control[:60] = True
    X = rng.normal(size=(n_wells, n_dims)) + np.array([5.0] * n_dims)
    out = typical_variation_normalization(X, is_control=is_control)
    # Controls should have approximately zero mean per dim after PCA whitening
    assert np.allclose(out[is_control].mean(axis=0), 0, atol=1e-6)


def test_tvn_unit_variance_on_controls():
    rng = np.random.default_rng(7)
    n_wells, n_dims = 500, 8
    is_control = np.zeros(n_wells, dtype=bool)
    is_control[:200] = True
    X = rng.normal(size=(n_wells, n_dims), scale=3.0)
    out = typical_variation_normalization(X, is_control=is_control)
    assert np.allclose(out[is_control].std(axis=0), 1, atol=0.1)


def test_tvn_preserves_shape_when_controls_exceed_dims():
    # rxrx3-core has ~25K EMPTY_control wells vs 384-1664 embedding dims, so
    # the realistic case is n_controls >> n_dims.
    rng = np.random.default_rng(0)
    n_wells, n_dims = 200, 16
    is_control = np.zeros(n_wells, dtype=bool)
    is_control[:60] = True
    X = rng.normal(size=(n_wells, n_dims))
    out = typical_variation_normalization(X, is_control=is_control)
    assert out.shape == X.shape


def test_tvn_clamps_n_components_when_controls_below_dims():
    # If a caller has fewer control wells than embedding dims, n_components
    # is clamped to min(n_controls, n_dims) so PCA can be fit.
    rng = np.random.default_rng(0)
    n_wells, n_dims = 100, 32
    is_control = np.zeros(n_wells, dtype=bool)
    is_control[:30] = True
    X = rng.normal(size=(n_wells, n_dims))
    out = typical_variation_normalization(X, is_control=is_control)
    assert out.shape == (n_wells, 30)


def test_tvn_with_explicit_n_components():
    rng = np.random.default_rng(0)
    n_wells, n_dims = 100, 32
    is_control = np.zeros(n_wells, dtype=bool)
    is_control[:50] = True
    X = rng.normal(size=(n_wells, n_dims))
    out = typical_variation_normalization(X, is_control=is_control, n_components=8)
    assert out.shape == (n_wells, 8)
