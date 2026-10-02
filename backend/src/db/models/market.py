from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional


class MarketPoint(BaseModel):
    record_date: datetime = Field(..., description="Date of the point")
    value: Decimal = Field(..., description="Price (assets) or rate to EUR (currencies)")


class MarketItemView(BaseModel):
    kind: str = Field(..., description="'asset' (market price) or 'rate' (currency exchange)")
    id: str = Field(..., description="Asset UUID for 'asset', currency code for 'rate'")
    name: str = Field(..., description="Display name")
    currency: str = Field(..., description="Currency code")
    icon_base64: Optional[str] = Field(None, description="Asset icon encoded in Base64, if any")
    value: Optional[Decimal] = Field(None, description="Latest value")
    date: Optional[datetime] = Field(None, description="Date of the latest value")
    points: list[MarketPoint] = Field(default_factory=list, description="Last N points, chronological")
