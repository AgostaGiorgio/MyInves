from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class SingleMonthChange(BaseModel):
    asset_name: str = Field(..., description="Name of the asset")
    asset_icon: Optional[str] = Field(None, description="The asset icon encoded in Base64 (e.g. data:image/png;base64,...)")
    month: str = Field(..., description="Month label (e.g. '2026-07') for the change")
    change_pct: Decimal = Field(..., description="Month-over-month percentage change")

class BestAssetResult(BaseModel):
    asset_name: str = Field(..., description="Name of the asset")
    asset_icon: Optional[str] = Field(None, description="The asset icon encoded in Base64 (e.g. data:image/png;base64,...)")
    growth_pct: Decimal = Field(..., description="Growth percentage")

class StatisticsResponse(BaseModel):
    current_total_eur: Decimal = Field(..., description="Current total net worth in EUR")
    change_vs_prev_month_pct: Optional[Decimal] = Field(None, description="Percentage change vs the previous month snapshot")
    avg_monthly_growth_pct: Optional[Decimal] = Field(None, description="Average month-over-month growth of the total portfolio")
    best_growth_to_date: Optional[BestAssetResult] = Field(None, description="Asset with the highest growth to date")
    best_single_month: Optional[SingleMonthChange] = Field(None, description="Largest single-month increase across all assets")
    worst_single_month: Optional[SingleMonthChange] = Field(None, description="Lowest single-month percentage across all assets (negative if a loss)")
