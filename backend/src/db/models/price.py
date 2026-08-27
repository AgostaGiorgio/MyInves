from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class AssetPrice(BaseModel):
    id: UUID = Field(..., description="ID univoco generato dal DB")
    asset_id: UUID = Field(..., description="L'asset a cui appartiene il prezzo")
    record_date: datetime = Field(..., description="La data del prezzo")
    price: Decimal = Field(..., description="Il prezzo registrato")

class AssetPriceCreate(BaseModel):
    record_date: datetime = Field(..., description="La data del prezzo")
    price: Decimal = Field(..., description="Il prezzo registrato")

class AssetPriceUpdate(BaseModel):
    record_date: datetime = Field(..., description="La data del prezzo")
    price: Decimal = Field(..., description="Il prezzo registrato")
