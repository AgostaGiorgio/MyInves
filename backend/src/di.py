from dependency_injector import containers, providers
from src.services.portfolio_service import PortfolioService

class Container(containers.DeclarativeContainer):

    portfolio_service = providers.Factory(PortfolioService)