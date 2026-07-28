from providers.universe.wikipedia_provider import WikipediaProvider


class WikipediaDJIAProvider(WikipediaProvider):
    URL = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    TABLE_INDEX = 1
    TICKER_COLUMN = "Symbol"
    COMPANY_COLUMN = "Company"
    SECTOR_COLUMN = "Sector"
    INDUSTRY_COLUMN = None
