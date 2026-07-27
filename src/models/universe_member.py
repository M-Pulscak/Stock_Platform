from dataclasses import dataclass


@dataclass(slots=True)
class UniverseMember:
    ticker: str
    company_name: str
    sector: str | None = None
    industry: str | None = None