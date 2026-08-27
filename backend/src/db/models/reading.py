from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID

class ReadingCreate(BaseModel):
    asset_id: UUID = Field(..., description="The ID of the asset this reading refers to")
    quantity: Decimal = Field(..., description="The quantity held on this date")
    
    def to_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "quantity": self.quantity
        }