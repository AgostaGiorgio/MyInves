from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID

class ReadingCreate(BaseModel):
    asset_id: UUID = Field(..., description="L'ID dell'asset a cui si riferisce")
    quantity: Decimal = Field(..., description="La quantità posseduta in questa data")
    
    def to_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "quantity": self.quantity
        }