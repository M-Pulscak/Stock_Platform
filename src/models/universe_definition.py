from dataclasses import dataclass

from models.universe import Universe
from providers.universe.universe_provider import UniverseProvider


@dataclass(slots=True)
class UniverseDefinition:
    universe: Universe
    provider: type[UniverseProvider]
