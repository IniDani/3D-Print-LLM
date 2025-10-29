import math
from src.tools.geometry import geometry_3d
from src.tools.estimate_cost import estimate_cost

def test_end_to_end_cylinder_to_cost():
    # Cylinder r=10mm, h=100mm
    vol = geometry_3d.invoke({
        "shape": "cylinder",
        "op": "volume",
        "dimensions": {"r": 10, "h": 100},
        "units": "mm",
    })
    assert vol["unit"] == "mm^3"
    volume_mm3 = vol["value"]
    expected_volume = math.pi * (10**2) * 100  # ≈ 31415.926 mm^3
    assert abs(volume_mm3 - expected_volume) < 1e-6

    cost = estimate_cost.invoke({
        "volume_mm3": volume_mm3,
        "material": "PLA",
        "infill_percent": 20,
    })
    # Perhitungan kasar: eff_vol ≈ 6283.185; mass ≈ 7.7932 g; price ≈ 4675.9
    assert cost["material"] == "PLA"
    assert cost["estimated_cost_idr"] > 0
    assert abs(cost["estimated_cost_idr"] - 4676) < 10  # toleransi pembulatan
