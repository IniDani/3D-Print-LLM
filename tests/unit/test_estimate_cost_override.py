from src.tools.estimate_cost import estimate_cost

def test_estimate_cost_with_overrides():
    # volume=50000, infill=50% → eff_vol=25000
    # density=0.002 → mass=50 g; rate=1000 → cost=50000
    out = estimate_cost.invoke({
        "volume_mm3": 50_000,
        "material": "PLA",                # material tetap, tapi kita override
        "infill_percent": 50,
        "density_g_per_mm3": 0.002,
        "rate_idr_per_g": 1000.0,
    })
    assert abs(out["mass_g"] - 50.0) < 1e-6
    assert out["estimated_cost_idr"] == 50_000.0
    assert out["rate_idr_per_g"] == 1000.0
