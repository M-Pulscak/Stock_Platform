from db.database import Database
from providers.yahoo import YahooProvider
from repositories.asset_repository import AssetRepository
from repositories.asset_type_repository import AssetTypeRepository
from repositories.currency_repository import CurrencyRepository
from repositories.exchange_repository import ExchangeRepository
from importers.assets import AssetImporter
from utils.logger import get_logger


class AssetSyncService:

    def __init__(self, db: Database):
        self.logger = get_logger("AssetSyncService")
        provider = YahooProvider()
        exchange_repo = ExchangeRepository(db)
        currency_repo = CurrencyRepository(db)
        asset_type_repo = AssetTypeRepository(db)
        asset_repo = AssetRepository(
            db,
            exchange_repo,
            currency_repo,
            asset_type_repo,
        )
        self.asset_importer = AssetImporter(
            provider,
            asset_repo,
        )

    def run(self, tickers: set[str]) -> None:
        total = len(tickers)
        self.logger.info(
            "Synchronizing %d asset(s)...",
            total,
        )

        for index, ticker in enumerate(sorted(tickers), start=1):
            self.logger.info(
                "[%d/%d] %s",
                index,
                total,
                ticker,
            )
            self.asset_importer.import_ticker(ticker)
        self.logger.info(
            "Asset synchronization finished."
        )
