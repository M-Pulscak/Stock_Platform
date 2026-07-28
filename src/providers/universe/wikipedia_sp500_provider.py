from providers.universe.wikipedia_provider import WikipediaProvider


class WikipediaSP500Provider(WikipediaProvider):
    URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    TABLE_INDEX = 0
    TICKER_COLUMN = "Symbol"
    COMPANY_COLUMN = "Security"
    SECTOR_COLUMN = "GICS Sector"
    INDUSTRY_COLUMN = "GICS Sub-Industry"
