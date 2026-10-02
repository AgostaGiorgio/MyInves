from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID

class ReadingCreate(BaseModel):
    asset_id: UUID = Field(..., description="The ID of the asset this reading refers to")
    quantity: Decimal = Field(..., description="The quantity held on this date")
    cost_price: Optional[Decimal] = Field(
        default=None,
        description="Average cost per unit (asset currency) at this reading; null if unknown",
    )
    
    def to_dict(self) -> dict:
        return {
            "asset_id": str(self.asset_id),
            "quantity": str(self.quantity),
            "cost_price": str(self.cost_price) if self.cost_price is not None else None,
        }
