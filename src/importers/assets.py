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
        Imports or updates a single asset.

        Parameters
        ----------
        ticker : str
            Market ticker symbol.

        Returns
        -------
        int
            Asset ID.
        """

        self._logger.info("Importing ticker %s", ticker)
        asset = self._provider.get_asset(ticker)
        asset_id = self._asset_repository.upsert(asset)
        self._logger.info(
            "Asset synchronized %s (asset_id=%s)",
            ticker,
            asset_id,
        )

        return asset_id
