import io
from abc import ABC
import pandas as pd
import requests
from models.universe_member import UniverseMember
from providers.universe.universe_provider import UniverseProvider


class WikipediaProvider(UniverseProvider, ABC):

    URL: str = ""
    TABLE_INDEX: int = 0
    TICKER_COLUMN: str = ""
    COMPANY_COLUMN: str = ""
    SECTOR_COLUMN: str | None = None
    INDUSTRY_COLUMN: str | None = None

    def get_members(self) -> list[UniverseMember]:
        response = requests.get(
            self.URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30,
        )
        response.raise_for_status()
        tables = pd.read_html(io.StringIO(response.text))
        df = tables[self.TABLE_INDEX]
        members: list[UniverseMember] = []

        for _, row in df.iterrows():
            members.append(
                UniverseMember(
                    ticker=self.normalize_ticker(
                        row[self.TICKER_COLUMN]
                    ),
                    company_name=row[self.COMPANY_COLUMN],
                    sector=(
                        row[self.SECTOR_COLUMN]
                        if self.SECTOR_COLUMN
                        else None
                    ),
                    industry=(
                        row[self.INDUSTRY_COLUMN]
                        if self.INDUSTRY_COLUMN
                        else None
                    ),
                )
            )
        return members

    @staticmethod
    def normalize_ticker(ticker: str) -> str:
        """
        Yahoo používá pomlčku místo tečky.
        Např. BRK.B -> BRK-B
        """

        return ticker.replace(".", "-")
