from db.database import Database
from providers.yahoo import YahooProvider
from repositories.exchange_repository import ExchangeRepository
from repositories.currency_repository import CurrencyRepository
from repositories.asset_type_repository import AssetTypeRepository
from repositories.asset_repository import AssetRepository
from repositories.price_repository import PriceRepository
from importers.assets import AssetImporter
from importers.prices import PriceImporter
from utils.logger import get_logger


class MarketImportService:

    def __init__(self, db: Database):
        self.db = db
        self.logger = get_logger("MarketImportService")
        self.provider = YahooProvider()
        exchange_repo = ExchangeRepository(db)
        currency_repo = CurrencyRepository(db)
        asset_type_repo = AssetTypeRepository(db)
        self.asset_repo = AssetRepository(
            db,
            exchange_repo,
            currency_repo,
            asset_type_repo,
        )
        self.price_repo = PriceRepository(db)
        self.asset_importer = AssetImporter(
            self.provider,
            self.asset_repo,
        )
        self.price_importer = PriceImporter(
            self.provider,
            self.asset_repo,
            self.price_repo,
        )

    def run(self, tickers: set[str]) -> None:
        self.logger.info(
            "Importing %d ticker(s)...",
            len(tickers),
        )
        for ticker in sorted(tickers):
            self.logger.info(
                "Processing %s",
                ticker,
            )
            asset_id = self.asset_importer.import_ticker(ticker)
            self.logger.debug(
                "Asset id = %s",
                asset_id,
            )
            self.price_importer.import_ticker(ticker)
        self.logger.info("Market import finished.")
