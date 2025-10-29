from src.tools.estimate_cost import estimate_cost

def test_estimate_cost_default_pla():
    # volume padat 100000 mm^3, infill 25% → eff_vol = 25000
    # densitas PLA 0.00124 → mass = 31.0 g → harga = 31 * 600 = 18600
    out = estimate_cost.invoke({
        "volume_mm3": 100_000,
        "material": "PLA",
        "infill_percent": 25,
    })
    assert out["material"] == "PLA"
    assert out["effective_volume_mm3"] == 25_000
    assert abs(out["mass_g"] - 31.0) < 1e-6
    assert out["estimated_cost_idr"] == 18600.0
