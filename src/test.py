from db.database import Database
from repositories.universe_repository import UniverseRepository
from models.universe import Universe


with Database() as db:

    repo = UniverseRepository(db)

    universe = repo.get_or_create(
        Universe(
            universe_id=None,
            code="SP500",
            name="S&P 500",
            provider="Wikipedia",
        )
    )

    print(universe)