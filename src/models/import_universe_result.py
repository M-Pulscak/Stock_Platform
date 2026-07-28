from dataclasses import dataclass, field


@dataclass(slots=True)
class ImportUniverseResult:
    tickers: set[str] = field(default_factory=set)

    universes_processed: int = 0
    companies_processed: int = 0
