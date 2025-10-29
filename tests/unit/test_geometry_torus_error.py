import pytest
from src.tools.geometry import geometry_3d

def test_torus_invalid_R_le_r_raises():
    with pytest.raises(Exception):
        geometry_3d.invoke({
            "shape": "torus",
            "op": "volume",
            "dimensions": {"R": 10, "r": 12},  # invalid: R <= r
            "units": "mm",
        })
