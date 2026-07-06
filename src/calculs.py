# src/calculs.py
# Fonctions de calcul géospatial

def calculate_ndvi(nir: float, red: float) -> float:
    """Calcule le NDVI à partir des bandes NIR et Rouge."""
    if (nir + red) == 0:
        raise ValueError("La somme NIR + Rouge ne peut pas être zéro.")
    return (nir - red) / (nir + red)


def convert_surface_ha(surface_m2: float) -> float:
    """Convertit une superficie de m² en hectares."""
    if surface_m2 < 0:
        raise ValueError("La superficie ne peut pas être négative.")
    return surface_m2 / 10_000