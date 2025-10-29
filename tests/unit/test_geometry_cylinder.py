import math
from src.tools.geometry import geometry_3d

def test_cylinder_volume_from_cm():
    # r=2 cm → 20 mm; h=5 cm → 50 mm
    out = geometry_3d.invoke({
        "shape": "cylinder",
        "op": "volume",
        "dimensions": {"r": 2, "h": 5},
        "units": "cm",
    })
    expected = math.pi * (20**2) * 50  # π r^2 h (mm^3)
    assert out["unit"] == "mm^3"
    assert abs(out["value"] - expected) < 1e-6
