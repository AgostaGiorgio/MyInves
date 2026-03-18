import logging
from src.db.db import AsyncSessionLocal
from uuid import UUID
from datetime import datetime
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon, Period, HistoryItemView, AssetHistoryItemView
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate
from src.services.queries import *

logger = logging.getLogger(__name__)

class PortfolioRepository:

    @classmethod
    async def get_exchange_rates(cls) -> list[ExchangeRate]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_EXCHANGE_RATES)
                rates = result.mappings().all()
                logger.debug(f"Fetched {len(rates)} exchange rates from the database.")
                return [ExchangeRate(**rate) for rate in rates]
            except Exception as e:
                logger.error(f"Error fetching exchange rates: {e}")
                return []
        return []

    @classmethod
    async def create_asset(cls, asset_data: Asset) -> Asset | None:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(NEW_ASSET, asset_data.to_dict())
                
                    if result.rowcount > 0:
                        new_id = result.scalar()
                        logger.debug(f"Asset '{asset_data.name}' successfully created.")
                        asset_data.id = new_id
                        return asset_data
            except Exception as e:
                logger.error(f"Error creating asset '{asset_data.name}': {e}")
                return None
        return None
    
    @classmethod
    async def get_assets(cls) -> list[AssetWithPrice]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ASSETS)
                assets = result.mappings().all()
                logger.debug(f"Fetched {len(assets)} assets from the database.")
                return [AssetWithPrice(**asset) for asset in assets]
            except Exception as e:
                logger.error(f"Error fetching assets: {e}")
                return []
        return []
    
    @classmethod
    async def get_asset_icon(cls, id: UUID) -> AssetIcon | None:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ASSET_ICON, {"id": str(id)})
                asset = result.mappings().one()
                logger.debug(f"Fetched assets icon the database.")
                return AssetIcon(**asset)
            except Exception as e:
                logger.error(f"Error fetching assets icon: {e}")
                return None
        return None
    
    @classmethod
    async def get_asset_history(cls) -> list[AssetHistoryItemView]:
        history: dict[str, AssetHistoryItemView] = {}
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(ASSETS_HISTORY)
                assets = result.mappings().all()
                logger.debug(f"Fetched {len(assets)} assets history from the database.")
                
                for asset in assets:
                    history_item = HistoryItemView(**asset)
                    if asset["name"] in history:
                        history[asset["name"]].values.append(history_item)
                    else:
                        history[asset["name"]] = AssetHistoryItemView(
                            asset_name=asset["name"],
                            values=[history_item]
                        )
                        
                current_portfolio = await cls.get_portfolio()
                for asset in current_portfolio:
                    history_item = HistoryItemView(record_date=asset.reading_date, total_value_eur=asset.total_value_eur)
                    if asset.name in history:
                        history[asset.name].values.append(history_item)
                    else:
                        history[asset.name] = AssetHistoryItemView(
                            asset_name=asset.name,
                            values=[history_item]
                        )
                return history.values()
            except Exception as e:
                logger.error(f"Error fetching assets history: {e}")
                return []
        return history.values()
    
    @classmethod
    async def get_current_portfolio_total(cls) -> HistoryItemView | None:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_PORTFOLIO)
                assets = result.mappings().all()
                logger.debug(f"Fetched {len(assets)} portfolio assets from the database.")
                return  HistoryItemView(total_value_eur=sum([float(asset["total_value_eur"]) for asset in assets]), record_date=datetime.now())
            except Exception as e:
                logger.error(f"Error fetching portfolio: {e}")
                return None
        return None
    
    @classmethod
    async def get_portfolio(cls) -> list[PortfolioItemView]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_PORTFOLIO)
                assets = result.mappings().all()
                logger.debug(f"Fetched {len(assets)} portfolio assets from the database.")
                return [PortfolioItemView(**asset) for asset in assets]
            except Exception as e:
                logger.error(f"Error fetching portfolio: {e}")
                return []
        return []
        
    @classmethod
    async def get_portfolio_history(cls, period: Period) -> list[HistoryItemView]:
        history = []
        async with AsyncSessionLocal() as session:
            try:
                query, params = get_portfolio_history_query(period)
                result = await session.execute(query, params)
                assets = result.mappings().all()
                logger.debug(f"Fetched {len(assets)} portfolio history from the database.")
                history = [HistoryItemView(**asset) for asset in assets]
                logger.debug("Fetching current portfolio total...")
                current_total = await cls.get_current_portfolio_total()
                history.append(current_total)
            except Exception as e:
                logger.error(f"Error fetching portfolio history: {e}")
        return history

    @classmethod
    async def create_readings(cls, readings: list[ReadingCreate]) -> list[ReadingCreate] | None:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(NEW_READING, [r.to_dict() for r in readings])
                    logger.debug(f"Added {result.rowcount} new readings")
                    return readings
            except Exception as e:
                logger.error(f"Error creating new readings '{readings}': {e}")
                return None
        return None