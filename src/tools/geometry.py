from typing import Dict, Literal
from pydantic import BaseModel, Field
from math import pi, sqrt
from langchain_core.tools import tool

# ------- Args schema (untuk function calling) -------
class GeometryArgs(BaseModel):
    shape: Literal[
        "sphere","cube","cuboid","cylinder","cone",
        "triangular_prism","square_pyramid","rectangular_pyramid","torus"
    ] = Field(..., description="Nama bentuk 3D")
    op: Literal["volume","surface_area"] = "volume"
    dimensions: Dict[str, float] = Field(..., description="Parameter numerik (bisa pakai alias)")
    units: Literal["mm","cm"] = "mm"

# ------- Helpers -------
def _to_mm(x, units):  # konversi dimensi ke mm
    return x * 10 if units == "cm" else x

def _need(keys, d: Dict[str, float]):
    missing = [k for k in keys if d.get(k) is None]
    if missing:
        raise ValueError(
            f"Parameter kurang: {', '.join(missing)}. "
            "Balok: length/width/height atau l/w/h; Tabung: r/h; Kubus: a."
        )
    vals = [float(d[k]) for k in keys]
    if any(v <= 0 for v in vals):
        raise ValueError("Semua dimensi harus > 0.")
    return vals

def _normalize_dims(shape: str, dims: Dict[str, float]) -> Dict[str, float]:
    raw = {k.strip().lower(): v for k, v in dims.items()}
    alias = {
        "r": ["r","radius","jari","jari2","jari-jari"],
        "R": ["R","r_major","major_radius","radius_utama"],
        "a": ["a","side","sisi"],
        "b": ["b","base","alas"],
        "l": ["l","length","long","panjang","x"],
        "w": ["w","width","lebar","y"],
        "h": ["h","height","tinggi","z","t"],
    }

    def pick(key):
        for k in alias.get(key, [key]):
            if k in raw:
                return float(raw[k])
        return None

    out = {}
    s = shape.lower()
    if s == "sphere": out["r"] = pick("r")
    elif s in {"cuboid","rectangular_prism","rectangular_pyramid"}:
        out["l"], out["w"], out["h"] = pick("l"), pick("w"), pick("h")
    elif s in {"cylinder","cone"}:
        out["r"], out["h"] = pick("r"), pick("h")
    elif s == "cube": out["a"] = pick("a")
    elif s == "square_pyramid": out["a"], out["h"] = pick("a"), pick("h")
    elif s == "triangular_prism": out["b"], out["h"], out["l"] = pick("b"), pick("h"), pick("l")
    elif s == "torus":
        out["R"] = raw.get("R") or raw.get("r_major") or raw.get("major_radius")
        out["R"] = float(out["R"]) if out["R"] is not None else None
        out["r"] = pick("r")
    return out

# ------- TOOL -------
@tool("geometry_3d", args_schema=GeometryArgs)
def geometry_3d(shape: str, op: str, dimensions: Dict[str, float], units: str = "mm"):
    """Hitung volume/luas permukaan; input mm/cm; output mm²/mm³."""
    shape = shape.lower()
    dims_std = _normalize_dims(shape, dimensions)
    p = {k: _to_mm(v, units) for k, v in dims_std.items() if v is not None}

    if shape == "sphere":
        (r,) = _need(["r"], p); A = 4*pi*r**2; V=(4/3)*pi*r**3
    elif shape in {"cuboid","rectangular_prism"}:
        l,w,h = _need(["l","w","h"], p); A=2*(l*w + l*h + w*h); V=l*w*h
    elif shape == "cube":
        (a,) = _need(["a"], p); A=6*a*a; V=a**3
    elif shape == "cylinder":
        r,h = _need(["r","h"], p); A=2*pi*r*(r+h); V=pi*r*r*h
    elif shape == "cone":
        r,h = _need(["r","h"], p); s=sqrt(r*r+h*h); A=pi*r*(r+s); V=(pi*r*r*h)/3
    elif shape == "triangular_prism":
        b,h,l = _need(["b","h","l"], p); A_base=0.5*b*h; perim=b+h+sqrt(b*b+h*h); A=2*A_base+perim*l; V=A_base*l
    elif shape == "square_pyramid":
        a,h = _need(["a","h"], p); s=sqrt((a/2)**2 + h**2); A=a*a + 2*a*s; V=(a*a*h)/3
    elif shape == "rectangular_pyramid":
        l,w,h = _need(["l","w","h"], p); s_l=sqrt((w/2)**2+h**2); s_w=sqrt((l/2)**2+h**2); A=l*w + l*s_l + w*s_w; V=(l*w*h)/3
    elif shape == "torus":
        if p.get("R") is None or p.get("r") is None:
            raise ValueError("Torus butuh R (major radius) dan r (minor radius).")
        R, r = float(p["R"]), float(p["r"])
        if R <= r: raise ValueError("Untuk torus, R harus > r.")
        A = 4*pi**2*R*r; V = 2*pi**2*R*r**2
    else:
        raise ValueError(f"Bentuk '{shape}' tidak dikenal.")

    value = V if op == "volume" else A
    unit = "mm^3" if op == "volume" else "mm^2"
    return {"shape": shape, "operation": op, "value": value, "unit": unit}
