from pydantic import BaseModel, Field

class Currency(BaseModel):
    code: str = Field(..., description="Currency code (e.g. EUR)")
    label: str = Field(..., description="Display name (e.g. Euro)")

class AssetType(BaseModel):
    code: str = Field(..., description="Asset type code (e.g. ETF)")
    label: str = Field(..., description="Display name (e.g. ETF)")

class CurrencyCreate(BaseModel):
    code: str = Field(..., description="Currency code (e.g. GBP)")
    label: str = Field(..., description="Display name (e.g. British Pound)")

class CurrencyLabelUpdate(BaseModel):
    label: str = Field(..., description="New display name of the currency")
