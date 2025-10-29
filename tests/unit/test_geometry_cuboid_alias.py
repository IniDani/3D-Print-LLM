from src.tools.geometry import geometry_3d

def test_cuboid_volume_with_aliases_in_cm():
    out = geometry_3d.invoke({
        "shape": "cuboid",
        "op": "volume",
        "dimensions": {"length": 15, "width": 7, "height": 1},  # cm
        "units": "cm",
    })
    # 15cm→150mm, 7cm→70mm, 1cm→10mm → V=150*70*10=105000 mm^3
    assert out["unit"] == "mm^3"
    assert out["value"] == 150 * 70 * 10
