from models.universe import Universe
from models.universe_definition import UniverseDefinition
from providers.universe.wikipedia_djia_provider import (
    WikipediaDJIAProvider,
)
from providers.universe.wikipedia_sp500_provider import (
    WikipediaSP500Provider,
)


class UniverseRegistry:
    def get_universes(self) -> list[UniverseDefinition]:
        return [
            UniverseDefinition(
                universe=Universe(
                    universe_id=None,
                    code="SP500",
                    name="S&P 500",
                    provider="Wikipedia",
                ),
                provider=WikipediaSP500Provider,
            ),
            UniverseDefinition(
                universe=Universe(
                    universe_id=None,
                    code="DJIA",
                    name="Dow Jones Industrial Average",
                    provider="Wikipedia",
                ),
                provider=WikipediaDJIAProvider,
            ),
        ]
