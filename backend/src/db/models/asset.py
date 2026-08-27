from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

Period = Literal["all", "3m", "6m", "12m"]
PERIOD_MONTHS = {
    "3m": 3,
    "6m": 6,
    "12m": 12,
}

class Asset(BaseModel):
    id: Optional[UUID] = Field(None, description="The unique ID in the database")
    name: str = Field(..., description="Asset name, e.g. 'Intesa Account', 'Bitcoin', 'VWCE'")
    asset_type: str = Field(..., description="The investment category (code in asset_types)")
    currency: str = Field(..., description="The base currency or unit of measure (code in currencies)")
    icon_base64: Optional[str] = Field(
        default=None, 
        description="The asset icon encoded in Base64 (e.g. data:image/png;base64,...)"
    )
    include_in_stats: bool = Field(
        default=False,
        description="Whether this asset should be included in the statistics calculations"
    )
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "asset_type": self.asset_type,
            "currency": self.currency,
            "icon_base64": self.icon_base64,
            "include_in_stats": self.include_in_stats
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
    
class HistoryItemView(BaseModel):
    record_date: datetime = Field(..., description="Reading date")
    total_value_eur: Decimal = Field(..., description="Total value converted to Euros")
    
class AssetHistoryItemView(BaseModel):
    asset_name: str
    values: list[HistoryItemView]