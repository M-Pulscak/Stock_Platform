from __future__ import annotations
from datetime import date
import yfinance as yf
from config import YAHOO_PRICE
from models.asset import Asset
from providers.yahoo.yahoo_mapper import YahooMapper
from providers.yahoo.yahoo_models import YahooPrice


class YahooProvider:
    """
    Provider for Yahoo Finance.
    Responsible only for communication with Yahoo Finance.
    Mapping of external data to domain models is delegated
    to YahooMapper.
    """

    def get_asset(
        self,
        ticker: str,
    ) -> Asset:
        """
        Returns a domain Asset object.

                Parameters
        ----------
        ticker : str
            Asset ticker (e.g. MSFT)

        Returns
        -------
        Asset
        """

        info = yf.Ticker(ticker).info
        return YahooMapper.to_asset(info)

    def get_price_history(
        self,
        ticker: str,
        start_date: date | None = None,
    ) -> list[YahooPrice]:
        """
        Returns historical daily prices.

        Parameters
        ----------
        ticker : str
            Asset ticker (e.g. MSFT)

        start_date : date | None
            If specified, downloads prices starting from this date.
            Otherwise downloads the configured history period.

        Returns
        -------
        list[YahooPrice]
        """

        yf_ticker = yf.Ticker(ticker)

        if start_date is None:
            history = yf_ticker.history(
                period=YAHOO_PRICE.history_period,
                auto_adjust=YAHOO_PRICE.auto_adjust,
                actions=YAHOO_PRICE.include_actions,
            )
        else:
            history = yf_ticker.history(
                start=start_date,
                auto_adjust=YAHOO_PRICE.auto_adjust,
                actions=YAHOO_PRICE.include_actions,
            )

        return YahooMapper.to_prices(history)
