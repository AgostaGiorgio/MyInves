from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime
from src.db.models.enums import CurrencyEnum, AssetTypeEnum

Period = Literal["all", "3m", "6m", "12m"]
PERIOD_MONTHS = {
    "3m": 3,
    "6m": 6,
    "12m": 12,
}

class Asset(BaseModel):
    id: Optional[UUID] = Field(None, description="L'ID univoco nel database")
    name: str = Field(..., description="Nome dell'asset, es. 'Conto Intesa', 'Bitcoin', 'VWCE'")
    asset_type: AssetTypeEnum = Field(..., description="La categoria dell'investimento")
    currency: CurrencyEnum = Field(..., description="La valuta di base o l'unità di misura")
    icon_base64: Optional[str] = Field(
        default=None, 
        description="L'icona dell'asset codificata in Base64 (es. data:image/png;base64,...)"
    )
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "asset_type": self.asset_type,
            "currency": self.currency,
            "icon_base64": self.icon_base64
        }
        
class AssetIcon(BaseModel):
    id: UUID = Field(..., description="L'ID univoco nel database")
    icon_base64: Optional[str] = Field(
        default=None, 
        description="L'icona dell'asset codificata in Base64 (es. data:image/png;base64,...)"
    )

class AssetWithPrice(Asset):
    price: Decimal = Field(..., description="Il prezzo attuale dell'asset in valuta di base")
    price_date: datetime = Field(..., description="La data dell'ultimo prezzo registrato")
    
class PortfolioItemView(BaseModel):
    id: UUID
    name: str
    asset_type: AssetTypeEnum
    currency: CurrencyEnum
    reading_date: datetime = Field(..., description="Data dell'ultima lettura inserita")
    quantity: Decimal = Field(..., description="Quantità dell'asset posseduta")
    total_value_eur: Decimal = Field(..., description="Valore totale convertito in Euro")
    
class HistoryItemView(BaseModel):
    record_date: datetime = Field(..., description="Data della lettura")
    total_value_eur: Decimal = Field(..., description="Valore totale convertito in Euro")
    
class AssetHistoryItemView(BaseModel):
    asset_name: str
    values: list[HistoryItemView]