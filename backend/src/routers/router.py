from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide
from src.di import Container
from uuid import UUID
from src.services.portfolio_service import PortfolioService
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon, HistoryItemView, Period, AssetHistoryItemView
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate, ExchangeRateCreate
from src.db.models.lookup import Currency, AssetType, CurrencyCreate, AssetTypeCreate, CurrencyLabelUpdate, AssetTypeLabelUpdate
from src.db.models.price import AssetPrice, AssetPriceCreate


api_router = APIRouter()

@api_router.get("/exchange-rates", response_model=list[ExchangeRate], status_code=200)
@inject
async def get_exchange_rates(asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[ExchangeRate]:
    return await asset_service.get_exchange_rates()

@api_router.get("/exchange-rates/all", response_model=list[ExchangeRate], status_code=200)
@inject
async def get_all_exchange_rates(asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[ExchangeRate]:
    return await asset_service.get_all_exchange_rates()

@api_router.post("/exchange-rates", response_model=ExchangeRate, status_code=201)
@inject
async def add_exchange_rate(rate: ExchangeRateCreate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> ExchangeRate:
    created: ExchangeRate | None = await asset_service.add_exchange_rate(rate)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to add exchange rate.")
    return created

@api_router.patch("/exchange-rates/{rate_id}", response_model=ExchangeRateCreate, status_code=200)
@inject
async def update_exchange_rate(rate_id: UUID, rate: ExchangeRateCreate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> ExchangeRateCreate:
    updated: bool = await asset_service.update_exchange_rate(rate_id, rate)
    if not updated:
        raise HTTPException(status_code=404, detail="Exchange rate not found.")
    return rate

@api_router.delete("/exchange-rates/{rate_id}", status_code=204)
@inject
async def delete_exchange_rate(rate_id: UUID, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> None:
    deleted: bool = await asset_service.delete_exchange_rate(rate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Exchange rate not found.")

@api_router.get("/assets", response_model=list[AssetWithPrice], status_code=200)
@inject
async def get_assets(portfolio_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[AssetWithPrice]:
    return await portfolio_service.get_assets()

@api_router.get("/assets/{id}/icon", response_model=AssetIcon, status_code=200)
@inject
async def get_asset_icon(id: UUID, portfolio_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> AssetIcon:
    return await portfolio_service.get_asset_icon(id)

@api_router.post("/assets", response_model=Asset, status_code=201)
@inject
async def create_asset(asset: Asset, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> Asset:
    new_asset: Asset | None = await asset_service.add_new_asset(asset)
    if not new_asset:
        raise HTTPException(status_code=400, detail="Failed to create asset.")
    return new_asset

@api_router.patch("/assets/{id}", response_model=Asset, status_code=200)
@inject
async def update_asset(id: UUID, asset: Asset, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> Asset:
    asset.id = id
    updated: Asset | None = await asset_service.update_asset(asset)
    if not updated:
        raise HTTPException(status_code=404, detail="Asset not found.")
    return updated

@api_router.get("/assets/{id}/prices", response_model=list[AssetPrice], status_code=200)
@inject
async def get_asset_prices(id: UUID, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[AssetPrice]:
    return await asset_service.get_asset_prices(id)

@api_router.post("/assets/{id}/prices", response_model=AssetPrice, status_code=201)
@inject
async def add_asset_price(id: UUID, price: AssetPriceCreate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> AssetPrice:
    created: AssetPrice | None = await asset_service.add_asset_price(id, price)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to add price.")
    return created

@api_router.patch("/prices/{price_id}", response_model=AssetPriceCreate, status_code=200)
@inject
async def update_asset_price(price_id: UUID, price: AssetPriceCreate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> AssetPriceCreate:
    updated: bool = await asset_service.update_asset_price(price_id, price)
    if not updated:
        raise HTTPException(status_code=404, detail="Price not found.")
    return price

@api_router.delete("/prices/{price_id}", status_code=204)
@inject
async def delete_asset_price(price_id: UUID, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> None:
    deleted: bool = await asset_service.delete_asset_price(price_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Price not found.")

@api_router.get("/assets/history", response_model=list[AssetHistoryItemView], status_code=200)
@inject
async def get_asset_history(asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[AssetHistoryItemView]:
    return await asset_service.get_asset_history()

@api_router.get("/portfolio", response_model=list[PortfolioItemView], status_code=200)
@inject
async def get_portfolio(portfolio_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[PortfolioItemView]:
    return await portfolio_service.get_portfolio()

@api_router.get("/portfolio/history", response_model=list[HistoryItemView], status_code=200)
@inject
async def get_portfolio_history(period: Period = Query("all"), portfolio_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[HistoryItemView]:
    return await portfolio_service.get_portfolio_history(period=period)

@api_router.post("/readings", response_model=list[ReadingCreate], status_code=201)
@inject
async def create_asset(readings: list[ReadingCreate], asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[ReadingCreate]:
    created_readings: Asset | None = await asset_service.add_readings(readings)
    if not created_readings:
        raise HTTPException(status_code=400, detail="Failed to create asset.")
    return created_readings

@api_router.post("/currencies", status_code=201)
@inject
async def create_currency(currency: CurrencyCreate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> CurrencyCreate:
    created: bool = await asset_service.add_currency(code=currency.code, label=currency.label)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create currency (maybe it already exists).")
    return currency

@api_router.post("/asset-types", status_code=201)
@inject
async def create_asset_type(asset_type: AssetTypeCreate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> AssetTypeCreate:
    created: bool = await asset_service.add_asset_type(code=asset_type.code, label=asset_type.label)
    if not created:
        raise HTTPException(status_code=400, detail="Failed to create asset type (maybe it already exists).")
    return asset_type

@api_router.get("/currencies", response_model=list[Currency], status_code=200)
@inject
async def get_currencies(asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[Currency]:
    return await asset_service.get_currencies()

@api_router.get("/asset-types", response_model=list[AssetType], status_code=200)
@inject
async def get_asset_types(asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[AssetType]:
    return await asset_service.get_asset_types()

@api_router.patch("/currencies/{code}", response_model=Currency, status_code=200)
@inject
async def rename_currency(code: str, update: CurrencyLabelUpdate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> Currency:
    renamed: bool = await asset_service.rename_currency(code=code, label=update.label)
    if not renamed:
        raise HTTPException(status_code=404, detail="Currency not found.")
    return Currency(code=code, label=update.label)

@api_router.patch("/asset-types/{code}", response_model=AssetType, status_code=200)
@inject
async def rename_asset_type(code: str, update: AssetTypeLabelUpdate, asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> AssetType:
    renamed: bool = await asset_service.rename_asset_type(code=code, label=update.label)
    if not renamed:
        raise HTTPException(status_code=404, detail="Asset type not found.")
    return AssetType(code=code, label=update.label)