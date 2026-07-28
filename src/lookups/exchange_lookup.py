from typing import Final


class UnknownExchangeError(ValueError):
    """Raised when a Yahoo exchange cannot be mapped to a MIC code."""


class ExchangeLookup:
    """
    Converts provider-specific exchange codes to ISO 10383 MIC codes.
    """

    _YAHOO_TO_MIC: Final[dict[str, str]] = {
        "NMS": "XNAS",   # Nasdaq Global Select / Global Market
        "NGM": "XNGM",   # Nasdaq Global Market
        "NYQ": "XNYS",   # New York Stock Exchange
        "ASE": "XASE",   # NYSE American
        "PCX": "ARCX",   # NYSE Arca
        "BTS": "BATS",   # Cboe BZX
    }

    @classmethod
    def yahoo_to_mic(cls, yahoo_code: str) -> str:
        """
        Convert Yahoo exchange code to ISO 10383 MIC.

        Raises:
            UnknownExchangeError: if mapping does not exist.
        """

        try:
            return cls._YAHOO_TO_MIC[yahoo_code]
        except KeyError as ex:
            raise UnknownExchangeError(
                f"Unknown Yahoo exchange code: '{yahoo_code}'"
            ) from ex
