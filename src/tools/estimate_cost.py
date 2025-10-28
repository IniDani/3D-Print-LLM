from typing import Optional, Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class CostArgs(BaseModel):
    volume_mm3: float = Field(..., gt=0, description="Total volume padat model (mm^3)")
    material: Literal["PLA", "ABS"] = "PLA"
    infill_percent: float = Field(
        20, ge=0, le=100, description="Persentase pengisian (0-100). Tidak termasuk shell/wall."
    )
    # Opsional override (kalau mau uji coba harga/tipe material lain)
    rate_idr_per_g: Optional[float] = Field(
        None, description="Tarif harga (Rp/gram). Jika None, gunakan default by material."
    )
    density_g_per_mm3: Optional[float] = Field(
        None, description="Massa jenis (gram/mm^3). Jika None, gunakan default by material."
    )



# Default Filament Parameter
DEFAULT_DENSITY = {  # gram per mm^3
    "PLA": 0.00124,  # 1.24 g/cm^3 = 0.00124 g/mm^3
    "ABS": 0.00107,  # 1.07 g/cm^3 = 0.00107 g/mm^3
}

DEFAULT_RATE_IDR_PER_G = {  # Rupiah per gram
    "PLA": 600.0,
    "ABS": 800.0,
}



@tool("estimate_cost", args_schema=CostArgs)
def estimate_cost(
    volume_mm3: float,
    material: str = "PLA",
    infill_percent: float = 20,
    rate_idr_per_g: float | None = None,
    density_g_per_mm3: float | None = None,
):
    """
    Estimasi biaya cetak berbasis MASSA:
    1) effective_volume = volume_mm3 * (infill_percent / 100)
    2) mass_g = effective_volume * density_g_per_mm3
    3) cost = mass_g * rate_idr_per_g

    Default:
      - Densitas: PLA=0.00124 g/mm^3, ABS=0.00107 g/mm^3
      - Rate:     PLA=Rp600/g,      ABS=Rp800/g

    Catatan: volume yang digunakan adalah volume padat model (mm^3).
    Jika Anda ingin memasukkan shell/wall thickness, tambahkan ke volume terlebih dahulu.
    """
    mat = material.upper()
    if mat not in DEFAULT_DENSITY:
        raise ValueError("Material tidak didukung. Gunakan 'PLA' atau 'ABS'.")

    density = density_g_per_mm3 if density_g_per_mm3 is not None else DEFAULT_DENSITY[mat]
    rate = rate_idr_per_g if rate_idr_per_g is not None else DEFAULT_RATE_IDR_PER_G[mat]

    # Effective volume dari infill (boleh 0 jika user set 0%)
    eff_vol = volume_mm3 * (max(min(infill_percent, 100.0), 0.0) / 100.0)

    # Berat dalam gram
    mass_g = eff_vol * density

    # Biaya
    cost_idr = mass_g * rate

    return {
        "material": mat,
        "input_volume_mm3": volume_mm3,
        "infill_percent": infill_percent,
        "effective_volume_mm3": eff_vol,
        "density_g_per_mm3": density,
        "mass_g": round(mass_g, 4),
        "rate_idr_per_g": rate,
        "estimated_cost_idr": round(cost_idr, 2),
        "notes": "Estimasi berbasis massa (eff. volume × densitas × rate).",
    }