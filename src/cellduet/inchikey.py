"""InChIKey computation from SMILES, used for cross-dataset compound joining."""

from typing import Literal

from rdkit import Chem


def compute_inchikey(
    smiles: str,
    key_type: Literal["full", "skeleton"] = "full",
) -> str | None:
    """Compute the InChIKey for a SMILES string.

    Returns None for unparseable SMILES. Skeleton key is the first 14 chars
    (connectivity layer only); full key is 27 chars (connectivity, stereochemistry,
    and protonation).
    """
    if key_type not in ("full", "skeleton"):
        raise ValueError(f"key_type must be 'full' or 'skeleton', got {key_type!r}")
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    full = Chem.MolToInchiKey(mol)
    return full if key_type == "full" else full[:14]
