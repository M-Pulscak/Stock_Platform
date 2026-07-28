from providers.universe.wikipedia_provider import WikipediaProvider


class WikipediaNasdaq100Provider(WikipediaProvider):
    URL = "https://en.wikipedia.org/wiki/Nasdaq-100"
    TABLE_INDEX = 4
    TICKER_COLUMN = "Ticker"
    COMPANY_COLUMN = "Company"
    SECTOR_COLUMN = "GICS Sector"
    INDUSTRY_COLUMN = "GICS Sub-Industry"
