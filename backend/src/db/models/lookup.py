from pydantic import BaseModel, Field

class CurrencyCreate(BaseModel):
    code: str = Field(..., description="Codice valuta (es. GBP)")
    label: str = Field(..., description="Nome visualizzato (es. Sterlina britannica)")

class AssetTypeCreate(BaseModel):
    code: str = Field(..., description="Codice tipo asset (es. BOND)")
    label: str = Field(..., description="Nome visualizzato (es. Obbligazione)")
