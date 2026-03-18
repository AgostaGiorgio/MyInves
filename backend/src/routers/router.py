from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide
from src.di import Container
from uuid import UUID
from src.services.portfolio_service import PortfolioService
from src.db.models.asset import Asset, AssetWithPrice, PortfolioItemView, AssetIcon, HistoryItemView, Period, AssetHistoryItemView
from src.db.models.reading import ReadingCreate
from src.db.models.exchange import ExchangeRate


api_router = APIRouter()

@api_router.get("/exchange-rates", response_model=list[ExchangeRate], status_code=200)
@inject
async def get_exchange_rates(asset_service: PortfolioService = Depends(Provide[Container.portfolio_service])) -> list[ExchangeRate]:
    return await asset_service.get_exchange_rates()

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