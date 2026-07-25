from services.yahoo_price import YahooPriceService
from mappers.price_mapper import PriceMapper
from repositories.asset_repository import AssetRepository
from repositories.price_repository import PriceRepository
from utils.logger import get_logger


class PriceImporter:
    """
    Imports historical prices from Yahoo Finance into PostgreSQL.
    """

    def __init__(
        self,
        yahoo_price_service: YahooPriceService,
        price_mapper: PriceMapper,
        asset_repository: AssetRepository,
        price_repository: PriceRepository,
    ):
        self._yahoo_price_service = yahoo_price_service
        self._price_mapper = price_mapper
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

        yahoo_prices = self._yahoo_price_service.get_history(ticker)

        count = 0

        for yahoo_price in yahoo_prices:

            price = self._price_mapper.map(
                asset_id=asset_id,
                yahoo_price=yahoo_price,
            )

            self._price_repository.upsert(price)
            count += 1

        self._logger.info(
            "Imported %s daily prices for %s",
            count,
            ticker,
        )

        return count
