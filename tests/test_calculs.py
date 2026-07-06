# tests/test_calculs.py
# Tests unitaires pour src/calculs.py

import pytest
from src.calculs import calculate_ndvi, convert_surface_ha


def test_ndvi_healthy_vegetation():
    """Végétation saine : NIR fort, rouge faible → NDVI positif."""
    assert calculate_ndvi(nir=0.8, red=0.1) > 0


def test_ndvi_exact_calculation():
    """(0.8 - 0.2) / (0.8 + 0.2) = 0.6."""
    assert calculate_ndvi(nir=0.8, red=0.2) == pytest.approx(0.6)


def test_ndvi_division_by_zero():
    """NIR = rouge = 0 doit lever une ValueError."""
    with pytest.raises(ValueError):
        calculate_ndvi(nir=0.0, red=0.0)


def test_surface_conversion():
    """10 000 m² = 1 ha."""
    assert convert_surface_ha(10_000) == pytest.approx(1.0)


def test_surface_negative():
    """Surface négative doit lever une ValueError."""
    with pytest.raises(ValueError):
        convert_surface_ha(-500)