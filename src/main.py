from db.database import Database
from models.universe import Universe
from providers.universe.wikipedia_sp500_provider import WikipediaSP500Provider
from services.universe_importer import UniverseImporter


with Database() as db:

    importer = UniverseImporter(
        db=db,
        universe=Universe(
            universe_id=None,
            code="SP500",
            name="S&P 500",
            provider="Wikipedia",
        ),
        provider=WikipediaSP500Provider(),
    )

    universe = importer.import_universe()

    print(universe)