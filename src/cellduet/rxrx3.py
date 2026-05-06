"""rxrx3-core loader, OpenPhenom embedding fetch, and EFAAR-style TVN.

The rxrx3-core release ships per-well embeddings (OpenPhenom 384-d,
Phenom-1 1024-d, Phenom-2 1664-d) on Hugging Face under the Recursion
EULA (CC-BY-SA-like with a hard neuroscience carve-out). See
docs/datasets/rxrx3.md.

Typical Variation Normalization is a PCA-whitening on EMPTY_control
wells, applied to all wells, after which the control wells have zero
mean and unit variance per latent dimension. Reference: Kraus et al.
arXiv:2503.20158, and Recursion's EFAAR_benchmarking library.
"""
from typing import Optional

import numpy as np
from sklearn.decomposition import PCA


def typical_variation_normalization(
    X: np.ndarray,
    is_control: np.ndarray,
    n_components: Optional[int] = None,
) -> np.ndarray:
    """EFAAR-style TVN: PCA-fit on controls, project all wells, whiten.

    Parameters
    ----------
    X : array of shape (n_wells, n_dims)
        Per-well embedding matrix.
    is_control : boolean array of length n_wells
        True for EMPTY_control (or other matched control) wells.
    n_components : int, optional
        Latent dimensionality. Defaults to n_dims.

    Returns
    -------
    array of shape (n_wells, n_components or n_dims)
        TVN-projected embedding. Control wells have zero mean and unit
        variance per dimension by construction.
    """
    if X.ndim != 2:
        raise ValueError(f"X must be 2-D, got shape {X.shape}")
    if is_control.shape[0] != X.shape[0]:
        raise ValueError(
            f"is_control length {is_control.shape[0]} must equal X rows {X.shape[0]}"
        )
    if not is_control.any():
        raise ValueError("is_control must mark at least one row as a control well")

    n_controls = int(is_control.sum())
    if n_components is None:
        n_components = min(n_controls, X.shape[1])
    pca = PCA(n_components=n_components, whiten=True)
    pca.fit(X[is_control])
    return pca.transform(X)
