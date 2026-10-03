import logging
from src.db.db import AsyncSessionLocal
from uuid import UUID
from datetime import datetime, timezone
from decimal import Decimal
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon, Period, HistoryItemView, AssetHistoryItemView
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate
from src.db.models.lookup import Currency, AssetType
from src.db.models.price import AssetPrice
from src.db.models.order import AssetOrder, AssetOrderCreate
from src.db.models.enums import OrderSide
from src.db.models.market import MarketItemView, MarketPoint
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
    async def get_all_exchange_rates(cls) -> list[ExchangeRate]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ALL_EXCHANGE_RATES)
                rates = result.mappings().all()
                logger.debug(f"Fetched {len(rates)} exchange rates from the database.")
                return [ExchangeRate(**rate) for rate in rates]
            except Exception as e:
                logger.error(f"Error fetching exchange rates: {e}")
                return []
        return []

    @classmethod
    async def add_exchange_rate(cls, currency: str, record_date: datetime, rate_to_eur) -> ExchangeRate | None:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        NEW_EXCHANGE_RATE,
                        {"currency": currency, "record_date": record_date, "rate_to_eur": str(rate_to_eur)},
                    )
                    new_id = result.scalar()
                    logger.debug(f"Exchange rate for '{currency}' added.")
                    return ExchangeRate(id=new_id, currency=currency, record_date=record_date, rate_to_eur=rate_to_eur)
            except Exception as e:
                logger.error(f"Error adding exchange rate for '{currency}': {e}")
                return None
        return None

    @classmethod
    async def update_exchange_rate(cls, rate_id: UUID, currency: str, record_date: datetime, rate_to_eur) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        UPDATE_EXCHANGE_RATE,
                        {"id": str(rate_id), "currency": currency, "record_date": record_date, "rate_to_eur": str(rate_to_eur)},
                    )
                    if result.rowcount == 0:
                        return False
                    logger.debug(f"Exchange rate '{rate_id}' updated.")
                    return True
            except Exception as e:
                logger.error(f"Error updating exchange rate '{rate_id}': {e}")
                return False
        return False

    @classmethod
    async def delete_exchange_rate(cls, rate_id: UUID) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(DELETE_EXCHANGE_RATE, {"id": str(rate_id)})
                    if result.rowcount == 0:
                        return False
                    logger.debug(f"Exchange rate '{rate_id}' deleted.")
                    return True
            except Exception as e:
                logger.error(f"Error deleting exchange rate '{rate_id}': {e}")
                return False
        return False

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
    async def update_asset(cls, asset_data: Asset) -> Asset | None:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    params = {**asset_data.to_dict(), "id": str(asset_data.id)}
                    result = await session.execute(UPDATE_ASSET, params)
                    if result.rowcount == 0:
                        logger.warning(f"Asset '{asset_data.id}' not found.")
                        return None
                    logger.debug(f"Asset '{asset_data.name}' successfully updated.")
                    return asset_data
            except Exception as e:
                logger.error(f"Error updating asset '{asset_data.name}': {e}")
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
    async def get_asset_prices(cls, asset_id: UUID) -> list[AssetPrice]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ASSET_PRICES, {"asset_id": str(asset_id)})
                rows = result.mappings().all()
                return [AssetPrice(**row) for row in rows]
            except Exception as e:
                logger.error(f"Error fetching prices for asset '{asset_id}': {e}")
                return []
        return []

    @classmethod
    async def add_asset_price(cls, asset_id: UUID, record_date: datetime, price) -> AssetPrice | None:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        NEW_ASSET_PRICE,
                        {"asset_id": str(asset_id), "record_date": record_date, "price": str(price)},
                    )
                    new_id = result.scalar()
                    if new_id is None:
                        logger.warning(
                            f"Price not added for asset '{asset_id}': not found or type does not support market prices."
                        )
                        return None
                    logger.debug(f"Price added for asset '{asset_id}'.")
                    return AssetPrice(id=new_id, asset_id=asset_id, record_date=record_date, price=price)
            except Exception as e:
                logger.error(f"Error adding price for asset '{asset_id}': {e}")
                return None
        return None

    @classmethod
    async def get_asset_type(cls, asset_id: UUID) -> str | None:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ASSET_TYPE, {"id": str(asset_id)})
                row = result.scalar()
                return row
            except Exception as e:
                logger.error(f"Error fetching type for asset '{asset_id}': {e}")
                return None
        return None

    @classmethod
    async def get_asset_orders(cls, asset_id: UUID) -> list[AssetOrder]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ASSET_ORDERS, {"asset_id": str(asset_id)})
                rows = result.mappings().all()
                return [AssetOrder(**row) for row in rows]
            except Exception as e:
                logger.error(f"Error fetching orders for asset '{asset_id}': {e}")
                return []
        return []

    @classmethod
    async def create_order(cls, asset_id: UUID, data: AssetOrderCreate, order_date: datetime) -> AssetOrder | None:
        """Registra un ordine e aggiorna la lettura della posizione con il
        nuovo costo medio pesato (per un BUY), tutto in una transazione."""
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    prev = (await session.execute(
                        GET_LATEST_READING, {"asset_id": str(asset_id)}
                    )).mappings().first()

                    prev_qty = Decimal(prev["quantity"]) if prev else Decimal("0")
                    prev_cost = (
                        Decimal(prev["cost_price"]) if prev and prev["cost_price"] is not None else None
                    )

                    qty = Decimal(data.quantity)
                    amount = Decimal(data.amount_invested)

                    if data.side == OrderSide.BUY:
                        new_qty = prev_qty + qty
                        if prev_qty > 0 and prev_cost is not None:
                            new_cost = (prev_qty * prev_cost + amount) / new_qty
                        elif qty > 0:
                            new_cost = amount / qty
                        else:
                            new_cost = prev_cost
                    else:
                        new_qty = prev_qty - qty
                        new_cost = prev_cost

                    if new_cost is not None:
                        new_cost = new_cost.quantize(Decimal("0.00000001"))

                    params = {
                        "asset_id": str(asset_id),
                        "order_date": order_date,
                        "side": data.side.value,
                        "quantity": str(qty),
                        "amount_invested": str(amount),
                        "fees": str(data.fees),
                        "note": data.note,
                    }
                    result = await session.execute(NEW_ASSET_ORDER, params)
                    row = result.mappings().one()

                    await session.execute(
                        NEW_READING_ON_DATE,
                        {
                            "asset_id": str(asset_id),
                            "record_date": row["order_date"],
                            "quantity": str(new_qty),
                            "cost_price": str(new_cost) if new_cost is not None else None,
                        },
                    )

                    logger.debug(
                        f"Order registered for asset '{asset_id}': qty={qty} side={data.side.value}, "
                        f"position {prev_qty} -> {new_qty}, avg cost {new_cost}."
                    )
                    return AssetOrder(
                        id=row["id"],
                        asset_id=asset_id,
                        order_date=row["order_date"],
                        side=data.side,
                        quantity=qty,
                        amount_invested=amount,
                        fees=data.fees,
                        note=data.note,
                    )
            except Exception as e:
                logger.error(f"Error registering order for asset '{asset_id}': {e}")
                return None
        return None

    @classmethod
    async def delete_order(cls, asset_id: UUID, order_id: UUID) -> bool:
        """Elimina un ordine e ricalcola la posizione replicando il ledger
        rimanente a partire dall'ultima lettura manuale."""
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    deleted = await session.execute(
                        DELETE_ASSET_ORDER, {"id": str(order_id), "asset_id": str(asset_id)}
                    )
                    if deleted.rowcount == 0:
                        logger.warning(f"Order '{order_id}' not found for asset '{asset_id}'.")
                        return False

                    # Base: ultima lettura inserita manualmente.
                    manual = (await session.execute(
                        GET_LATEST_MANUAL_READING, {"asset_id": str(asset_id)}
                    )).mappings().first()
                    qty = Decimal(manual["quantity"]) if manual else Decimal("0")
                    cost = Decimal(manual["cost_price"]) if manual and manual["cost_price"] is not None else None

                    # Rigenera la posizione replicando gli ordini rimasti.
                    await session.execute(DELETE_ORDER_READINGS, {"asset_id": str(asset_id)})
                    orders = (await session.execute(
                        GET_ASSET_ORDERS_ASC, {"asset_id": str(asset_id)}
                    )).mappings().all()

                    for order in orders:
                        o_qty = Decimal(order["quantity"])
                        amount = Decimal(order["amount_invested"])
                        if order["side"] == OrderSide.BUY.value:
                            new_qty = qty + o_qty
                            if qty > 0 and cost is not None:
                                cost = (qty * cost + amount) / new_qty
                            elif o_qty > 0:
                                cost = amount / o_qty
                            qty = new_qty
                        else:
                            qty = qty - o_qty

                    if cost is not None:
                        cost = cost.quantize(Decimal("0.00000001"))

                    await session.execute(
                        NEW_READING_ON_DATE,
                        {
                            "asset_id": str(asset_id),
                            "record_date": datetime.now(timezone.utc),
                            "quantity": str(qty),
                            "cost_price": str(cost) if cost is not None else None,
                        },
                    )
                    logger.debug(
                        f"Order '{order_id}' deleted for asset '{asset_id}': "
                        f"replayed {len(orders)} orders -> position {qty}, avg cost {cost}."
                    )
                    return True
            except Exception as e:
                logger.error(f"Error deleting order '{order_id}' for asset '{asset_id}': {e}")
                return False
        return False

    @classmethod
    async def update_asset_price(cls, price_id: UUID, record_date: datetime, price) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(
                        UPDATE_ASSET_PRICE,
                        {"id": str(price_id), "record_date": record_date, "price": str(price)},
                    )
                    if result.rowcount == 0:
                        return False
                    logger.debug(f"Price '{price_id}' updated.")
                    return True
            except Exception as e:
                logger.error(f"Error updating price '{price_id}': {e}")
                return False
        return False

    @classmethod
    async def delete_asset_price(cls, price_id: UUID) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(DELETE_ASSET_PRICE, {"id": str(price_id)})
                    if result.rowcount == 0:
                        return False
                    logger.debug(f"Price '{price_id}' deleted.")
                    return True
            except Exception as e:
                logger.error(f"Error deleting price '{price_id}': {e}")
                return False
        return False
    
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
    async def get_market_history(cls, points: int) -> list[MarketItemView]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_MARKET_HISTORY, {"points": points})
                rows = result.mappings().all()
            except Exception as e:
                logger.error(f"Error fetching market history: {e}")
                return []

        # Raggruppa per item: le righe arrivano per item in ordine cronologico.
        grouped: dict[tuple, MarketItemView] = {}
        for row in rows:
            key = (row["kind"], row["item_id"])
            item = grouped.get(key)
            if item is None:
                item = MarketItemView(
                    kind=row["kind"],
                    id=row["item_id"],
                    name=row["name"],
                    currency=row["currency"],
                    icon_base64=row["icon_base64"],
                )
                grouped[key] = item
            item.points.append(MarketPoint(record_date=row["record_date"], value=row["value"]))

        for item in grouped.values():
            if item.points:
                item.value = item.points[-1].value
                item.date = item.points[-1].record_date

        logger.debug(f"Fetched market history for {len(grouped)} items (points={points}).")
        return list(grouped.values())
    
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
    async def get_all_portfolio_history(cls) -> list[HistoryItemView]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ALL_PORTFOLIO_HISTORY)
                rows = result.mappings().all()
                logger.debug(f"Fetched {len(rows)} portfolio history rows from the database.")
                return [HistoryItemView(**row) for row in rows]
            except Exception as e:
                logger.error(f"Error fetching all portfolio history: {e}")
                return []
        return []

    @classmethod
    async def get_all_assets_history(cls) -> dict[str, list[HistoryItemView]]:
        history: dict[str, list[HistoryItemView]] = {}
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ALL_ASSETS_HISTORY)
                rows = result.mappings().all()
                logger.debug(f"Fetched {len(rows)} assets history rows from the database.")
                for row in rows:
                    item = HistoryItemView(record_date=row["record_date"], total_value_eur=row["total_value_eur"])
                    history.setdefault(row["name"], []).append(item)
            except Exception as e:
                logger.error(f"Error fetching all assets history: {e}")
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

    @classmethod
    async def add_currency(cls, code: str, label: str) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    await session.execute(NEW_CURRENCY, {"code": code, "label": label})
                    logger.debug(f"Currency '{code}' successfully created.")
                    return True
            except Exception as e:
                logger.error(f"Error creating currency '{code}': {e}")
                return False
        return False

    @classmethod
    async def get_currencies(cls) -> list[Currency]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_CURRENCIES)
                rows = result.mappings().all()
                return [Currency(**row) for row in rows]
            except Exception as e:
                logger.error(f"Error fetching currencies: {e}")
                return []
        return []

    @classmethod
    async def get_asset_types(cls) -> list[AssetType]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(GET_ASSET_TYPES)
                rows = result.mappings().all()
                return [AssetType(**row) for row in rows]
            except Exception as e:
                logger.error(f"Error fetching asset types: {e}")
                return []
        return []

    @classmethod
    async def rename_currency(cls, code: str, label: str) -> bool:
        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    result = await session.execute(UPDATE_CURRENCY_LABEL, {"code": code, "label": label})
                    if result.rowcount == 0:
                        logger.warning(f"Currency '{code}' not found.")
                        return False
                    logger.debug(f"Currency '{code}' successfully renamed.")
                    return True
            except Exception as e:
                logger.error(f"Error renaming currency '{code}': {e}")
                return False
        return False