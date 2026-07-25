from providers.provider import MarketDataProvider
from repositories.asset_repository import AssetRepository
from repositories.price_repository import PriceRepository
from utils.logger import get_logger


class PriceImporter:
    """
    Imports historical prices from a market data provider into PostgreSQL.
    """

    def __init__(
        self,
        provider: MarketDataProvider,
        asset_repository: AssetRepository,
        price_repository: PriceRepository,
    ):
        self._provider = provider
        self._asset_repository = asset_repository
        self._price_repository = price_repository
        self._logger = get_logger(self.__class__.__name__)

    def import_ticker(
        self,
        ticker: str,
        exchange_mic: str | None = None,
    ) -> int:
        """
        Imports complete historical price series for one ticker.

        Returns
        -------
        int
            Number of imported trading days.
        """

        self._logger.info("Importing prices for %s", ticker)

        asset_id = self._asset_repository.get_by_ticker(
            ticker=ticker,
            exchange_mic=exchange_mic,
        )

        if asset_id is None:
            raise ValueError(
                f"Ticker '{ticker}' does not exist in core.assets."
            )

        prices = self._provider.get_price_history(ticker)

        count = 0

        for price in prices:

            # Provider vrací Price bez asset_id,
            # importer doplní vazbu na databázový záznam.
            price.asset_id = asset_id

            self._price_repository.upsert(price)

            count += 1

        self._logger.info(
            "Imported %s daily prices for %s",
            count,
            ticker,
        )

        return count
