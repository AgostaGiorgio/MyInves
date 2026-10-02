"""Dettagli specifici per tipo di asset.

I campi vivono in un'unica colonna `assets.details JSONB` e vengono validati
prima della scrittura con il modello corrispondente al tipo. `extra="forbid"`
fa si' che campi non pertinenti al tipo producano un 422 invece di essere
silenziosamente salvati.
"""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.db.models.enums import AssetType


class _DetailsBase(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class EtfDetails(_DetailsBase):
    isin: Optional[str] = None
    ticker: Optional[str] = None
    exchange: Optional[str] = None
    ter: Optional[Decimal] = None
    distribution_policy: Optional[str] = None  # accumulating | distributing


class CryptoDetails(_DetailsBase):
    symbol: Optional[str] = None
    chain: Optional[str] = None
    contract_address: Optional[str] = None
    broker: Optional[str] = None


class MetalDetails(_DetailsBase):
    metal: Optional[str] = None  # gold | silver
    form: Optional[str] = None  # bar | coin | jewelry | other
    purity: Optional[Decimal] = None
    weight_grams: Optional[Decimal] = None


class BankAccountDetails(_DetailsBase):
    bank_name: Optional[str] = None
    iban: Optional[str] = None
    interest_rate: Optional[Decimal] = None
    interest_frequency: Optional[str] = None  # monthly | quarterly | yearly


class CashDetails(_DetailsBase):
    location: Optional[str] = None
    notes: Optional[str] = None


class OtherDetails(_DetailsBase):
    category: Optional[str] = None
    notes: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_value: Optional[Decimal] = None


DETAILS_MODELS: dict[str, type[BaseModel]] = {
    AssetType.ETF.value: EtfDetails,
    AssetType.CRYPTO.value: CryptoDetails,
    AssetType.METAL.value: MetalDetails,
    AssetType.CASH.value: CashDetails,
    AssetType.BANK_ACCOUNT.value: BankAccountDetails,
    AssetType.BANK_ACCOUNT_STATIC.value: BankAccountDetails,
    AssetType.OTHER.value: OtherDetails,
}


def parse_details(asset_type: str, raw) -> dict:
    """Normalizza i dettagli per il tipo dato.

    Accetta dict (scrittura API) o stringa JSON (lettura dal DB). Lascia
    passare i tipi sconosciuti senza validazione per non bloccare dati legacy.
    """
    if raw is None:
        raw = {}
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    if isinstance(raw, str):
        raw = json.loads(raw) if raw.strip() else {}
    if not isinstance(raw, dict):
        raise ValueError("details deve essere un oggetto JSON")

    model = DETAILS_MODELS.get(asset_type)
    if model is None:
        return dict(raw)

    return model.model_validate(raw).model_dump(exclude_none=True)
