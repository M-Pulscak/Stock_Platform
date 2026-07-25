from __future__ import annotations
from typing import Any
import pandas as pd
from models.asset import Asset
from models.price import Price


class YahooMapper:
    """
    Maps Yahoo Finance responses
    to internal domain models.
    """

    @staticmethod
    def to_asset(info: dict[str, Any]) -> Asset:
        """
        Convert Yahoo company info to Asset.
        """

        symbol = info.get("symbol")
        if not isinstance(symbol, str) or not symbol:
            raise ValueError("Yahoo response does not contain a valid ticker symbol.")

        name = info.get("longName") or info.get("shortName")
        if not isinstance(name, str) or not name:
            raise ValueError(f"Yahoo response for '{symbol}' does not contain a company name.")

        exchange = info.get("exchange")
        if not isinstance(exchange, str) or not exchange:
            raise ValueError(f"Yahoo response for '{symbol}' does not contain an exchange.")

        currency = info.get("currency")
        if not isinstance(currency, str) or not currency:
            raise ValueError(f"Yahoo response for '{symbol}' does not contain a currency.")

        return Asset(
            ticker=symbol,
            provider_symbol=symbol,
            name=name,
            exchange_mic=exchange,      # TODO: převést Yahoo -> MIC pomocí ExchangeLookup
            currency_code=currency,
            asset_type="Stock",
        )

    @staticmethod
    def to_prices(history: pd.DataFrame) -> list[Price]:
        """
        Convert Yahoo price history to list[Price].
        """

        prices: list[Price] = []

        if history.empty:
            return prices

        for trade_date, row in history.iterrows():

            prices.append(
                Price(
                    trade_date=trade_date.date(),
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
            )

        return prices