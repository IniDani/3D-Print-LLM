from typing import Optional, Literal
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class CostArgs(BaseModel):
    volume_mm3: float = Field(..., gt=0)
    material: Literal["PLA","ABS"] = "PLA"
    infill_percent: float = Field(20, ge=0, le=100)
    rate_idr_per_mm3: Optional[float] = None

@tool("estimate_cost", args_schema=CostArgs)
def estimate_cost(
    volume_mm3: float,
    material: str = "PLA",
    infill_percent: float = 20,
    rate_idr_per_mm3: float | None = None,
):
    """Estimasi biaya = volume efektif × tarif. Default tarif PLA 0.12; ABS 0.15 (IDR/mm^3)."""
    base_rates = {"PLA": 0.12, "ABS": 0.15}
    rate = rate_idr_per_mm3 or base_rates[material]
    eff_vol = volume_mm3 * max(infill_percent/100.0, 0.01)  # minimal 1%
    cost = eff_vol * rate
    return {
        "material": material,
        "volume_mm3": volume_mm3,
        "infill_percent": infill_percent,
        "rate": rate,
        "estimated_cost_idr": round(cost, 2),
    }
