from dependency_injector import containers, providers
from src.clients.postgres_client import PostgresClient
from src.config.app_config import app_config
from src.repositories.portfolio import PortfolioRepository
from src.services.portfolio_service import PortfolioService

class Container(containers.DeclarativeContainer):

    postgres_client = providers.Singleton(PostgresClient, db_url=app_config.postgresql_connection_uri)
    portfolio_repository = providers.Factory(PortfolioRepository, postgres_client=postgres_client)
    portfolio_service = providers.Factory(PortfolioService, portfolio_repository=portfolio_repository)
