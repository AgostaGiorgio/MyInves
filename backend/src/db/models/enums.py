from enum import Enum


class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"
    AED = "AED"

class AssetTypeEnum(str, Enum):
    ETF = "ETF"
    CRYPTO = "CRYPTO"
    CASH = "CASH"
    GOLD = "GOLD"
    BANK_ACCOUNT = "BANK_ACCOUNT"