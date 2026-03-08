import logging
from uuid import UUID
from src.services.portfolio_repository import PortfolioRepository
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate

logger = logging.getLogger(__name__)

class PortfolioService:

    async def get_exchange_rates(self) -> list[ExchangeRate]:
        logger.debug("Fetching exchange rates...")
        rates = await PortfolioRepository.get_exchange_rates()
        logger.debug(f"Retrieved {len(rates)} exchange rates.")
        return rates

    async def add_new_asset(self, asset_data: Asset) -> Asset:
        logger.debug(f"Adding new asset: {asset_data.name}..")
        return await PortfolioRepository.create_asset(asset_data)
    
    async def get_assets(self) -> list[AssetWithPrice]:
        logger.debug("Fetching assets...")
        assets = await PortfolioRepository.get_assets()
        logger.debug(f"Retrieved {len(assets)} assets.")
        return assets
    
    async def get_asset_icon(self, id: UUID) -> AssetIcon:
        logger.debug("Fetching asset icon...")
        asset = await PortfolioRepository.get_asset_icon(id)
        logger.debug(f"Retrieved asset icon.")
        return asset
    
    async def get_portfolio(self) -> list[PortfolioItemView]:
        logger.debug("Fetching portfolio...")
        portfolio = await PortfolioRepository.get_portfolio()
        logger.debug(f"Retrieved {len(portfolio)} assets from portfolio.")
        return portfolio

    async def add_readings(self, readings: list[ReadingCreate]) -> list[ReadingCreate]:
        logger.debug(f"Adding new reading set: {readings}..")
        return await PortfolioRepository.create_readings(readings)
        