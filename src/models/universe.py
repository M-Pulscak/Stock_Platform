from dataclasses import dataclass


@dataclass(slots=True)
class Universe:
    universe_id: int | None
    code: str
    name: str
    provider: str
    enabled: bool = True
    sort_order: int = 0