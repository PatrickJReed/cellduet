"""Cross-modal phenotype concordance statistics for cellduet.

Three top-level tests, each comparing two square distance matrices (one
per modality) on the same shared-compound set:

- mantel(D1, D2): Pearson correlation of upper-triangle distances, with
  optional permutation p-value.
- rv_coefficient(D1, D2): an inner-product-based similarity between
  distance matrices treated as kernel matrices.
- neighborhood_jaccard(D1, D2, k): per-row Jaccard overlap of k-nearest-
  neighbor sets across modalities.

All three are scale-invariant and treat distances as symmetric.
"""

from collections.abc import Callable

import numpy as np


def _upper_triangle(D: np.ndarray) -> np.ndarray:
    """Return the upper-triangle (k=1) elements of a square matrix as a 1-D array."""
    return D[np.triu_indices_from(D, k=1)]


def mantel(
    D1: np.ndarray,
    D2: np.ndarray,
    n_permutations: int = 999,
    seed: int = 0,
) -> tuple[float, float]:
    """Mantel correlation between two square distance matrices.

    Parameters
    ----------
    D1, D2 : square arrays of identical shape
        Pairwise distance matrices.
    n_permutations : int
        Number of row/column permutations of D2 used to build the null
        distribution. If 0, p is returned as NaN.
    seed : int
        RNG seed.

    Returns
    -------
    (r, p) : tuple
        r is the Pearson correlation of the upper-triangle distance vectors.
        p is the two-sided permutation p-value, or NaN if n_permutations=0.
    """
    if D1.shape != D2.shape or D1.ndim != 2 or D1.shape[0] != D1.shape[1]:
        raise ValueError(
            f"D1 and D2 must be square matrices of equal shape, got {D1.shape} vs {D2.shape}"
        )
    v1 = _upper_triangle(D1)
    v2 = _upper_triangle(D2)
    r = float(np.corrcoef(v1, v2)[0, 1])
    if n_permutations <= 0:
        return r, float("nan")
    rng = np.random.default_rng(seed)
    n = D1.shape[0]
    null = np.empty(n_permutations)
    for i in range(n_permutations):
        perm = rng.permutation(n)
        v2_perm = _upper_triangle(D2[np.ix_(perm, perm)])
        null[i] = np.corrcoef(v1, v2_perm)[0, 1]
    p = float((np.abs(null) >= abs(r)).mean())
    return r, p


def rv_coefficient(D1: np.ndarray, D2: np.ndarray) -> float:
    """RV coefficient between two distance matrices treated as kernel matrices.

    The RV coefficient is the matrix analogue of the Pearson correlation:
    RV(A, B) = tr(A B) / sqrt(tr(A A) tr(B B)). Distances are converted to
    kernel form via -0.5 * D**2 so the RV is bounded in [0, 1] for
    Euclidean-like inputs.
    """
    if D1.shape != D2.shape:
        raise ValueError(f"shape mismatch: {D1.shape} vs {D2.shape}")
    A = -0.5 * D1**2
    B = -0.5 * D2**2
    num = float(np.sum(A * B))
    denom = float(np.sqrt(np.sum(A * A) * np.sum(B * B)))
    return num / denom if denom > 0 else 0.0


def neighborhood_jaccard(D1: np.ndarray, D2: np.ndarray, k: int = 10) -> np.ndarray:
    """Per-row Jaccard overlap of the k-nearest-neighbor sets in two matrices.

    For each row i, computes the Jaccard similarity between the set of
    k nearest neighbors of i in D1 and the same set in D2 (excluding i itself).

    Returns a 1-D array of length n with values in [0, 1].
    """
    if D1.shape != D2.shape:
        raise ValueError(f"shape mismatch: {D1.shape} vs {D2.shape}")
    n = D1.shape[0]
    nn1 = np.argsort(D1, axis=1)[:, 1 : k + 1]
    nn2 = np.argsort(D2, axis=1)[:, 1 : k + 1]
    out = np.empty(n, dtype=float)
    for i in range(n):
        a = set(nn1[i].tolist())
        b = set(nn2[i].tolist())
        union = len(a | b)
        out[i] = (len(a & b) / union) if union > 0 else 0.0
    return out


def permutation_null(
    D1: np.ndarray,
    D2: np.ndarray,
    statistic: Callable,
    n_permutations: int = 999,
    seed: int = 0,
) -> np.ndarray:
    """Build a null distribution of `statistic` under random row/col permutations of D2.

    `statistic` may be `mantel` (returns a tuple) or any callable returning
    a scalar; the first element of a tuple return is used as the statistic.
    """
    rng = np.random.default_rng(seed)
    n = D1.shape[0]
    null = np.empty(n_permutations)
    for i in range(n_permutations):
        perm = rng.permutation(n)
        D2_perm = D2[np.ix_(perm, perm)]
        if statistic is mantel:
            result, _ = statistic(D1, D2_perm, n_permutations=0)
        else:
            result = statistic(D1, D2_perm)
            if isinstance(result, tuple):
                result = result[0]
        null[i] = result
    return null
