from providers.provider import MarketDataProvider
from repositories.asset_repository import AssetRepository
from repositories.price_repository import PriceRepository
from models.price import Price
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
        Imports historical price series for one ticker.

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

        last_trade_date = self._price_repository.get_last_trade_date(asset_id)

        self._logger.info(
            "Last trading day in database: %s",
            last_trade_date if last_trade_date else "none",
        )

        yahoo_prices = self._provider.get_price_history(
            ticker=ticker,
            start_date=last_trade_date,
        )

        count = 0

        for yahoo_price in yahoo_prices:
            price = Price(
                asset_id=asset_id,
                trading_date=yahoo_price.trading_date,
                open=yahoo_price.open,
                high=yahoo_price.high,
                low=yahoo_price.low,
                close=yahoo_price.close,
                adjusted_close=yahoo_price.adjusted_close,
                volume=yahoo_price.volume,
            )

            self._price_repository.upsert(price)
            count += 1

        self._logger.info(
            "Imported %s trading days for %s",
            count,
            ticker,
        )

        return count
