from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from src.db.models.enums import CurrencyEnum

class ExchangeRate(BaseModel):
    id: Optional[UUID] = Field(default=None, description="ID univoco generato dal DB")
    currency: CurrencyEnum = Field(..., description="La valuta (es. USD, AED, GOLD_G)")
    record_date: datetime = Field(..., description="La data del tasso di cambio")
    rate_to_eur: Decimal = Field(..., description="Il valore in Euro di 1 unità di questa valuta")