import logging
from uuid import UUID
from src.services.portfolio_repository import PortfolioRepository
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon, HistoryItemView, Period, AssetHistoryItemView
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate, ExchangeRateCreate
from src.db.models.price import AssetPrice, AssetPriceCreate

logger = logging.getLogger(__name__)

class PortfolioService:

    async def get_exchange_rates(self) -> list[ExchangeRate]:
        logger.debug("Fetching exchange rates...")
        rates = await PortfolioRepository.get_exchange_rates()
        logger.debug(f"Retrieved {len(rates)} exchange rates.")
        return rates

    async def get_all_exchange_rates(self) -> list[ExchangeRate]:
        logger.debug("Fetching all exchange rates...")
        return await PortfolioRepository.get_all_exchange_rates()

    async def add_exchange_rate(self, data: ExchangeRateCreate) -> ExchangeRate:
        logger.debug(f"Adding exchange rate for {data.currency}...")
        return await PortfolioRepository.add_exchange_rate(data.currency, data.record_date, data.rate_to_eur)

    async def update_exchange_rate(self, rate_id: UUID, data: ExchangeRateCreate) -> bool:
        logger.debug(f"Updating exchange rate {rate_id}...")
        return await PortfolioRepository.update_exchange_rate(rate_id, data.currency, data.record_date, data.rate_to_eur)

    async def delete_exchange_rate(self, rate_id: UUID) -> bool:
        logger.debug(f"Deleting exchange rate {rate_id}...")
        return await PortfolioRepository.delete_exchange_rate(rate_id)

    async def add_new_asset(self, asset_data: Asset) -> Asset:
        logger.debug(f"Adding new asset: {asset_data.name}..")
        return await PortfolioRepository.create_asset(asset_data)

    async def update_asset(self, asset_data: Asset) -> Asset:
        logger.debug(f"Updating asset: {asset_data.name}..")
        return await PortfolioRepository.update_asset(asset_data)
    
    async def get_assets(self) -> list[AssetWithPrice]:
        logger.debug("Fetching assets...")
        assets = await PortfolioRepository.get_assets()
        logger.debug(f"Retrieved {len(assets)} assets.")
        return assets

    async def get_asset_prices(self, asset_id: UUID) -> list[AssetPrice]:
        logger.debug(f"Fetching prices for asset {asset_id}...")
        return await PortfolioRepository.get_asset_prices(asset_id)

    async def add_asset_price(self, asset_id: UUID, data: AssetPriceCreate) -> AssetPrice:
        logger.debug(f"Adding price for asset {asset_id}...")
        return await PortfolioRepository.add_asset_price(asset_id, data.record_date, data.price)

    async def update_asset_price(self, price_id: UUID, data: AssetPriceCreate) -> bool:
        logger.debug(f"Updating price {price_id}...")
        return await PortfolioRepository.update_asset_price(price_id, data.record_date, data.price)

    async def delete_asset_price(self, price_id: UUID) -> bool:
        logger.debug(f"Deleting price {price_id}...")
        return await PortfolioRepository.delete_asset_price(price_id)
    
    async def get_asset_icon(self, id: UUID) -> AssetIcon:
        logger.debug("Fetching asset icon...")
        asset = await PortfolioRepository.get_asset_icon(id)
        logger.debug(f"Retrieved asset icon.")
        return asset
    
    async def get_asset_history(self) -> list[AssetHistoryItemView]:
        logger.debug("Fetching assets history...")
        assets = await PortfolioRepository.get_asset_history()
        logger.debug(f"Retrieved {len(assets)} elements from assets history.")
        return assets
    
    async def get_portfolio(self) -> list[PortfolioItemView]:
        logger.debug("Fetching portfolio...")
        portfolio = await PortfolioRepository.get_portfolio()
        logger.debug(f"Retrieved {len(portfolio)} assets from portfolio.")
        return portfolio
    
    async def get_portfolio_history(self, period: Period) -> list[HistoryItemView]:
        logger.debug("Fetching portfolio history...")
        portfolio_history = await PortfolioRepository.get_portfolio_history(period=period)
        logger.debug(f"Retrieved {len(portfolio_history)} elements from portfolio history.")
        return portfolio_history

    async def add_readings(self, readings: list[ReadingCreate]) -> list[ReadingCreate]:
        logger.debug(f"Adding new reading set: {readings}..")
        return await PortfolioRepository.create_readings(readings)

    async def add_currency(self, code: str, label: str) -> bool:
        logger.debug(f"Adding new currency {code}..")
        return await PortfolioRepository.add_currency(code, label)

    async def add_asset_type(self, code: str, label: str) -> bool:
        logger.debug(f"Adding new asset type {code}..")
        return await PortfolioRepository.add_asset_type(code, label)

    async def get_currencies(self) -> list:
        logger.debug("Fetching currencies...")
        return await PortfolioRepository.get_currencies()

    async def get_asset_types(self) -> list:
        logger.debug("Fetching asset types...")
        return await PortfolioRepository.get_asset_types()

    async def rename_currency(self, code: str, label: str) -> bool:
        logger.debug(f"Renaming currency {code}..")
        return await PortfolioRepository.rename_currency(code, label)

    async def rename_asset_type(self, code: str, label: str) -> bool:
        logger.debug(f"Renaming asset type {code}..")
        return await PortfolioRepository.rename_asset_type(code, label)
        