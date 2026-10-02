from enum import Enum


class AssetType(str, Enum):
    """Catalogo chiuso dei tipi di asset supportati dalla piattaforma.

    Il set e' *fisso*: i codici sono mantenuti anche nella tabella di lookup
    `asset_types` (gestita via migrazioni) ma non sono piu' creabili a runtime.
    """

    ETF = "ETF"
    CRYPTO = "CRYPTO"
    METAL = "METAL"
    CASH = "CASH"
    BANK_ACCOUNT = "BANK_ACCOUNT"
    BANK_ACCOUNT_STATIC = "BANK_ACCOUNT_STATIC"
    OTHER = "OTHER"


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


# Codici dei tipi tracciati a *valore diretto*: la lettura e' il valore posseduto
# (in valuta asset), non una quantita' da moltiplicare per un prezzo di mercato.
VALUE_TRACKED_CODES: frozenset[str] = frozenset(
    {
        AssetType.CASH.value,
        AssetType.BANK_ACCOUNT.value,
        AssetType.BANK_ACCOUNT_STATIC.value,
        AssetType.OTHER.value,
    }
)

# Codici dei tipi che ammettono posizioni/ordini (quantita' x prezzo).
ORDER_TRACKED_CODES: frozenset[str] = frozenset(
    {
        AssetType.ETF.value,
        AssetType.CRYPTO.value,
        AssetType.METAL.value,
    }
)
