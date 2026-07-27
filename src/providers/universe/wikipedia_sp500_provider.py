import io
import requests
import pandas as pd

from providers.universe.universe_provider import UniverseProvider
from models.universe_member import UniverseMember


class WikipediaSP500Provider(UniverseProvider):

    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def get_members(self) -> list[UniverseMember]:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(self.URL, headers=headers, timeout=30)
        response.raise_for_status()

        df = pd.read_html(io.StringIO(response.text))[0]

        members = []

        for _, row in df.iterrows():
            members.append(
                UniverseMember(
                    index_code="SP500",
                    ticker=row["Symbol"].replace(".", "-"),
                    company_name=row["Security"],
                    sector=row["GICS Sector"],
                    industry=row["GICS Sub-Industry"],
                )
            )

        return members