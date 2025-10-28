from src.app import geometry_3d, estimate_cost

def test_cylinder_volume_mm_units():
    out = geometry_3d.invoke({"shape":"cylinder","op":"volume","dimensions":{"r":4,"h":10},"units":"cm"})
    assert "value" in out and out["value"] > 0

def test_cost_estimation_pla():
    out = estimate_cost.invoke({"volume_mm3": 500000, "material":"PLA", "infill_percent":20})
    assert out["estimated_cost_idr"] > 0