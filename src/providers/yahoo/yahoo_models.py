from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(slots=True)
class YahooPrice:
    """
    Historical daily price returned by Yahoo Finance.
    This is a provider-specific DTO used to transfer price data
    from YahooProvider to the importer. It intentionally does not
    contain any internal database identifiers.
    """

    trading_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    adjusted_close: Decimal
    volume: int
