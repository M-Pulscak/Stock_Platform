from db.database import Database
from providers.yahoo import YahooProvider
from repositories.asset_repository import AssetRepository
from repositories.asset_type_repository import AssetTypeRepository
from repositories.currency_repository import CurrencyRepository
from repositories.exchange_repository import ExchangeRepository
from repositories.price_repository import PriceRepository
from importers.prices import PriceImporter
from utils.logger import get_logger


class PriceImportService:

    def __init__(self):
        self.logger = get_logger("PriceImportService")

    def run(self, tickers: set[str]) -> None:
        total = len(tickers)
        self.logger.info(
            "Importing prices for %d asset(s)...",
            total,
        )
        provider = YahooProvider()
        for index, ticker in enumerate(sorted(tickers), start=1):
            self.logger.info(
                "[%d/%d] %s",
                index,
                total,
                ticker,
            )
            with Database() as db:
                exchange_repo = ExchangeRepository(db)
                currency_repo = CurrencyRepository(db)
                asset_type_repo = AssetTypeRepository(db)
                asset_repo = AssetRepository(
                    db,
                    exchange_repo,
                    currency_repo,
                    asset_type_repo,
                )
                price_repo = PriceRepository(db)
                importer = PriceImporter(
                    provider,
                    asset_repo,
                    price_repo,
                )
                importer.import_ticker(ticker)
            self.logger.info(
                "%s committed.",
                ticker,
            )

        self.logger.info(
            "Price import finished."
        )
