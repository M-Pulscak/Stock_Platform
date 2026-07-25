from providers.provider import MarketDataProvider
from repositories.asset_repository import AssetRepository
from utils.logger import get_logger


class AssetImporter:
    """
    Imports asset metadata from a market data provider into PostgreSQL.
    """

    def __init__(
        self,
        provider: MarketDataProvider,
        asset_repository: AssetRepository,
    ):
        self._provider = provider
        self._asset_repository = asset_repository
        self._logger = get_logger(self.__class__.__name__)

    def import_ticker(self, ticker: str) -> int:
        """
        Imports one ticker.

        Returns
        -------
        int
            Asset ID.
        """

        self._logger.info("Importing ticker %s", ticker)

        asset = self._provider.get_asset(ticker)

        asset_id = self._asset_repository.upsert(asset)

        self._logger.info(
            "Imported %s (asset_id=%s)",
            ticker,
            asset_id,
        )

        return asset_id

    def import_many(self, tickers: list[str]) -> list[int]:
        """
        Imports multiple tickers.
        """

        asset_ids: list[int] = []

        total = len(tickers)

        self._logger.info(
            "Starting batch import (%d tickers)",
            total,
        )

        for index, ticker in enumerate(tickers, start=1):

            self._logger.info(
                "[%d/%d] %s",
                index,
                total,
                ticker,
            )

            asset_ids.append(
                self.import_ticker(ticker)
            )

        self._logger.info("Batch import finished.")

        return asset_ids
