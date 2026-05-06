"""Tests for src/cellduet/inchikey.py."""
import pytest

from cellduet.inchikey import compute_inchikey


# Aspirin: SMILES -> known full InChIKey
ASPIRIN_SMILES = "CC(=O)OC1=CC=CC=C1C(=O)O"
ASPIRIN_FULL_INCHIKEY = "BSYNRYMUTXBXSQ-UHFFFAOYSA-N"
ASPIRIN_SKELETON_INCHIKEY = "BSYNRYMUTXBXSQ"


def test_compute_inchikey_full_returns_27_char_key():
    result = compute_inchikey(ASPIRIN_SMILES, key_type="full")
    assert result == ASPIRIN_FULL_INCHIKEY
    assert len(result) == 27


def test_compute_inchikey_skeleton_returns_first_block():
    result = compute_inchikey(ASPIRIN_SMILES, key_type="skeleton")
    assert result == ASPIRIN_SKELETON_INCHIKEY
    assert len(result) == 14


def test_compute_inchikey_invalid_smiles_returns_none():
    result = compute_inchikey("not a smiles", key_type="full")
    assert result is None


def test_compute_inchikey_invalid_key_type_raises():
    with pytest.raises(ValueError):
        compute_inchikey(ASPIRIN_SMILES, key_type="invalid")
