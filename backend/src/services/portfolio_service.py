import logging
from uuid import UUID
from datetime import datetime
from src.services.portfolio_repository import PortfolioRepository
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon, HistoryItemView, Period, AssetHistoryItemView
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate, ExchangeRateCreate
from src.db.models.price import AssetPrice, AssetPriceCreate
from src.db.models.statistics import StatisticsResponse, SingleMonthChange, BestAssetResult, AssetMonthlyAverage

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

    @staticmethod
    def _month_label(dt: datetime) -> str:
        return f"{dt.year}-{dt.month:02d}"

    @staticmethod
    def _pct(prev: float, curr: float) -> float | None:
        if prev == 0:
            return None
        return (curr - prev) / prev * 100.0

    async def get_statistics(self) -> StatisticsResponse:
        logger.debug("Computing statistics...")

        current_total_item = await PortfolioRepository.get_current_portfolio_total()
        current_total = float(current_total_item.total_value_eur)

        monthly = await PortfolioRepository.get_all_portfolio_history()

        series = [float(h.total_value_eur) for h in monthly]
        series.append(current_total)

        change_vs_prev = None
        if len(series) >= 2:
            change_vs_prev = self._pct(series[-2], series[-1])

        changes = [self._pct(series[i], series[i + 1]) for i in range(len(series) - 1)]
        changes = [c for c in changes if c is not None]
        avg_monthly = (sum(changes) / len(changes)) if changes else None

        assets_history = await PortfolioRepository.get_all_assets_history()
        portfolio = await PortfolioRepository.get_portfolio()
        assets = await PortfolioRepository.get_assets()

        current_by_name = {a.name: float(a.total_value_eur) for a in portfolio}
        icons_by_name = {a.name: a.icon_base64 for a in assets}
        include_by_name = {a.name: bool(a.include_in_stats) for a in assets}
        names = {n for n in (set(assets_history.keys()) | set(current_by_name.keys())) if include_by_name.get(n) is True}

        best_growth_to_date = None
        best_single_month = None
        worst_single_month = None
        global_best_pct = None
        global_worst_pct = None
        per_asset_avg_monthly = []

        for name in names:
            history_items = assets_history.get(name, [])
            pts = [float(h.total_value_eur) for h in history_items]
            if name in current_by_name:
                pts.append(current_by_name[name])

            if len(pts) >= 2:
                g = self._pct(pts[0], pts[-1])
                if g is not None and (best_growth_to_date is None or g > float(best_growth_to_date.growth_pct)):
                    best_growth_to_date = BestAssetResult(asset_name=name, asset_icon=icons_by_name.get(name), growth_pct=round(g, 2))

            dates = [h.record_date for h in history_items]
            if name in current_by_name:
                dates.append(datetime.now())

            monthly_changes = []
            for i in range(len(pts) - 1):
                c = self._pct(pts[i], pts[i + 1])
                if c is None:
                    continue
                monthly_changes.append(c)
                month = self._month_label(dates[i + 1])
                if global_best_pct is None or c > global_best_pct:
                    global_best_pct = c
                    best_single_month = SingleMonthChange(asset_name=name, asset_icon=icons_by_name.get(name), month=month, change_pct=round(c, 2))
                if global_worst_pct is None or c < global_worst_pct:
                    global_worst_pct = c
                    worst_single_month = SingleMonthChange(asset_name=name, asset_icon=icons_by_name.get(name), month=month, change_pct=round(c, 2))

            if monthly_changes:
                per_asset_avg_monthly.append(AssetMonthlyAverage(
                    asset_name=name,
                    asset_icon=icons_by_name.get(name),
                    avg_monthly_pct=round(sum(monthly_changes) / len(monthly_changes), 2),
                ))

        per_asset_avg_monthly.sort(key=lambda a: a.avg_monthly_pct if a.avg_monthly_pct is not None else 0, reverse=True)

        return StatisticsResponse(
            current_total_eur=round(current_total, 2),
            change_vs_prev_month_pct=round(change_vs_prev, 2) if change_vs_prev is not None else None,
            avg_monthly_growth_pct=round(avg_monthly, 2) if avg_monthly is not None else None,
            per_asset_avg_monthly=per_asset_avg_monthly,
            best_growth_to_date=best_growth_to_date,
            best_single_month=best_single_month,
            worst_single_month=worst_single_month,
        )
        