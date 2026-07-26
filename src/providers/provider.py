from __future__ import annotations
from datetime import date
from typing import Protocol
from models.asset import Asset
from providers.yahoo.yahoo_models import YahooPrice


class MarketDataProvider(Protocol):
    """
    Protocol for market data providers.
    Any provider implementing these methods can be used
    by the importers without inheritance.
    """

    def get_asset(self, ticker: str) -> Asset:
        """
        Return metadata for a single asset.
        """
        ...

    def get_price_history(
        self,
        ticker: str,
        start_date: date | None = None,
    ) -> list[YahooPrice]:
        ...
