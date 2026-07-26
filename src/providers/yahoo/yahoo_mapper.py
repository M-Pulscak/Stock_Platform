from __future__ import annotations
from decimal import Decimal
from typing import Any, cast
import pandas as pd
from pandas import Timestamp
from models.asset import Asset
from models.enums import AssetType
from providers.yahoo.yahoo_models import YahooPrice


class YahooMapper:
    """
    Maps Yahoo Finance responses to internal models.
    """

    @staticmethod
    def to_asset(info: dict[str, Any]) -> Asset:
        symbol = info.get("symbol")
        if not isinstance(symbol, str) or not symbol:
            raise ValueError("Yahoo response does not contain a valid ticker symbol.")
        name = info.get("longName") or info.get("shortName")
        if not isinstance(name, str) or not name:
            raise ValueError(f"Yahoo response for '{symbol}' does not contain company name.")
        exchange = info.get("exchange")
        if not isinstance(exchange, str) or not exchange:
            raise ValueError(f"Yahoo response for '{symbol}' does not contain exchange.")
        currency = info.get("currency")
        if not isinstance(currency, str) or not currency:
            raise ValueError(f"Yahoo response for '{symbol}' does not contain currency.")

        return Asset(
            ticker=symbol,
            provider_symbol=symbol,
            exchange_mic=exchange,          # TODO ExchangeLookup
            currency_code=currency,
            asset_type=AssetType.STOCK,
            name=name,
        )

    @staticmethod
    def to_prices(history: pd.DataFrame) -> list[YahooPrice]:
        prices: list[YahooPrice] = []
        if history.empty:
            return prices
        for trade_date, row in history.iterrows():
            trade_date = cast(Timestamp, trade_date)
            prices.append(
                YahooPrice(
                    trading_date=trade_date.date(),
                    open=Decimal(str(row["Open"])),
                    high=Decimal(str(row["High"])),
                    low=Decimal(str(row["Low"])),
                    close=Decimal(str(row["Close"])),
                    adjusted_close=Decimal(str(row["Close"])),
                    volume=int(row["Volume"]),
                )
            )

        return prices
