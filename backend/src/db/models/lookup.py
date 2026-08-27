from pydantic import BaseModel, Field

class Currency(BaseModel):
    code: str = Field(..., description="Codice valuta (es. EUR)")
    label: str = Field(..., description="Nome visualizzato (es. Euro)")

class AssetType(BaseModel):
    code: str = Field(..., description="Codice tipo asset (es. ETF)")
    label: str = Field(..., description="Nome visualizzato (es. ETF)")

class CurrencyCreate(BaseModel):
    code: str = Field(..., description="Codice valuta (es. GBP)")
    label: str = Field(..., description="Nome visualizzato (es. Sterlina britannica)")

class AssetTypeCreate(BaseModel):
    code: str = Field(..., description="Codice tipo asset (es. BOND)")
    label: str = Field(..., description="Nome visualizzato (es. Obbligazione)")

class CurrencyLabelUpdate(BaseModel):
    label: str = Field(..., description="Nuovo nome visualizzato della valuta")

class AssetTypeLabelUpdate(BaseModel):
    label: str = Field(..., description="Nuovo nome visualizzato del tipo asset")
