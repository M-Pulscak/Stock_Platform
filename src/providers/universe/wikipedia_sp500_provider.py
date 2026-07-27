import io

import pandas as pd
import requests

from models.universe_member import UniverseMember
from providers.universe.universe_provider import UniverseProvider


class WikipediaSP500Provider(UniverseProvider):

    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

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
        df = tables[0]

        members = [
            UniverseMember(
                ticker=row["Symbol"],
                company_name=row["Security"],
                sector=row["GICS Sector"],
                industry=row["GICS Sub-Industry"],
            )
            for _, row in df.iterrows()
        ]

        return members