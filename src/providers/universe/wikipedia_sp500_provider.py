from src.providers.universe.universe_provider import UniverseProvider
from src.models.universe_member import UniverseMember


class WikipediaSP500Provider(UniverseProvider):

    def get_members(self) -> list[UniverseMember]:
        return []