import json

from pydantic import BaseModel, Field, field_validator, model_validator
from decimal import Decimal
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

from src.db.models.details import parse_details
from src.db.models.enums import AssetType

Period = Literal["all", "3m", "6m", "12m"]
PERIOD_MONTHS = {
    "3m": 3,
    "6m": 6,
    "12m": 12,
}

_ASSET_TYPE_CODES = {t.value for t in AssetType}


class Asset(BaseModel):
    id: Optional[UUID] = Field(None, description="The unique ID in the database")
    name: str = Field(..., description="Asset name, e.g. 'Intesa Account', 'Bitcoin', 'VWCE'")
    asset_type: str = Field(..., description="The investment category (code in asset_types)")
    currency: str = Field(..., description="The base currency or unit of measure (code in currencies)")
    icon_base64: Optional[str] = Field(
        default=None, 
        description="The asset icon encoded in Base64 (e.g. data:image/png;base64,...)"
    )
    details: dict = Field(
        default_factory=dict,
        description="Type-specific metadata (validated per asset_type), e.g. ETF ISIN/ticker",
    )

    @field_validator("asset_type")
    @classmethod
    def _validate_asset_type(cls, value: str) -> str:
        code = value.strip().upper()
        if code not in _ASSET_TYPE_CODES:
            allowed = ", ".join(sorted(_ASSET_TYPE_CODES))
            raise ValueError(f"Unknown asset_type '{value}'. Allowed: {allowed}")
        return code

    @field_validator("details", mode="before")
    @classmethod
    def _coerce_details(cls, value):
        # Il driver puo' restituire il JSONB come dict oppure come stringa JSON.
        if value is None:
            return {}
        if isinstance(value, (bytes, bytearray)):
            value = value.decode("utf-8")
        if isinstance(value, str):
            return json.loads(value) if value.strip() else {}
        return value

    @model_validator(mode="after")
    def _normalize_details(self) -> "Asset":
        self.details = parse_details(self.asset_type, self.details)
        return self

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "asset_type": self.asset_type,
            "currency": self.currency,
            "icon_base64": self.icon_base64,
            "details": json.dumps(self.details, default=str),
        }
        
class AssetIcon(BaseModel):
    id: UUID = Field(..., description="The unique ID in the database")
    icon_base64: Optional[str] = Field(
        default=None, 
        description="The asset icon encoded in Base64 (e.g. data:image/png;base64,...)"
    )

class AssetWithPrice(Asset):
    price: Decimal = Field(..., description="The current price of the asset in its base currency")
    price_date: datetime = Field(..., description="The date of the last recorded price")
    
class PortfolioItemView(BaseModel):
    id: UUID
    name: str
    asset_type: str
    asset_label: str
    currency: str
    reading_date: Optional[datetime] = Field(None, description="Date of the last inserted reading")
    quantity: Decimal = Field(..., description="Quantity of the asset held")
    total_value_eur: Decimal = Field(..., description="Total value converted to Euros")
    cost_price: Optional[Decimal] = Field(None, description="Average cost per unit in the asset currency")
    cost_value_eur: Optional[Decimal] = Field(None, description="Total cost basis converted to Euros")
    unrealized_pl_eur: Optional[Decimal] = Field(None, description="Unrealized P&L in Euros")
    unrealized_pl_pct: Optional[Decimal] = Field(None, description="Unrealized P&L percentage")
    
class HistoryItemView(BaseModel):
    record_date: datetime = Field(..., description="Reading date")
    total_value_eur: Decimal = Field(..., description="Total value converted to Euros")
    
class AssetHistoryItemView(BaseModel):
    asset_name: str
    values: list[HistoryItemView]
