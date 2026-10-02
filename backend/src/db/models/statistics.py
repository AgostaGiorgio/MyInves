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

class AssetMonthlyAverage(BaseModel):
    asset_name: str = Field(..., description="Name of the asset")
    asset_icon: Optional[str] = Field(None, description="The asset icon encoded in Base64 (e.g. data:image/png;base64,...)")
    avg_monthly_pct: Decimal = Field(..., description="Average month-over-month percentage change for the asset")

class TypeAllocation(BaseModel):
    asset_type: str = Field(..., description="Asset type code (e.g. ETF)")
    label: str = Field(..., description="Human-readable asset type label")
    total_value_eur: Decimal = Field(..., description="Total value of this type in Euros")
    weight_pct: Decimal = Field(..., description="Share of the whole portfolio in percent")
    asset_count: int = Field(..., description="Number of assets of this type")
    cost_value_eur: Optional[Decimal] = Field(None, description="Total cost basis of this type in Euros")
    unrealized_pl_eur: Optional[Decimal] = Field(None, description="Unrealized P&L of this type in Euros")
    unrealized_pl_pct: Optional[Decimal] = Field(None, description="Average unrealized P&L percentage of this type")
    avg_monthly_pct: Optional[Decimal] = Field(None, description="Average monthly growth across assets of this type")

class StatisticsResponse(BaseModel):
    current_total_eur: Decimal = Field(..., description="Current total net worth in EUR")
    change_vs_prev_month_pct: Optional[Decimal] = Field(None, description="Percentage change vs the previous month snapshot")
    change_vs_prev_month_eur: Optional[Decimal] = Field(None, description="Absolute change vs the previous month snapshot in EUR")
    avg_monthly_growth_pct: Optional[Decimal] = Field(None, description="Average month-over-month growth of the total portfolio")
    per_asset_avg_monthly: list[AssetMonthlyAverage] = Field(default_factory=list, description="Average monthly growth for each asset included in statistics")
    best_growth_to_date: Optional[BestAssetResult] = Field(None, description="Asset with the highest growth to date")
    best_single_month: Optional[SingleMonthChange] = Field(None, description="Largest single-month increase across all assets")
    worst_single_month: Optional[SingleMonthChange] = Field(None, description="Lowest single-month percentage across all assets (negative if a loss)")
    allocation: list[TypeAllocation] = Field(default_factory=list, description="Portfolio breakdown per asset type")
