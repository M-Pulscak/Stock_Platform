from __future__ import annotations

from typing import Protocol

from models.asset import Asset
from models.price import Price


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

    def get_price_history(self, ticker: str) -> list[Price]:
        """
        Return historical daily prices.
        """
        ...
