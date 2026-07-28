from db.database import Database
from models.universe_sync_result import UniverseSyncResult
from providers.universe.universe_registry import UniverseRegistry
from services.universe_importer import UniverseImporter
from utils.logger import get_logger


class UniverseSyncService:

    def __init__(self, db: Database):
        self.db = db
        self.registry = UniverseRegistry()
        self.logger = get_logger("UniverseSyncService")

    def run(self) -> UniverseSyncResult:
        result = UniverseSyncResult()
        definitions = self.registry.get_universes()
        self.logger.info(
            "Synchronizing %d universe(s)...",
            len(definitions),
        )

        for definition in definitions:
            provider = definition.provider()
            importer = UniverseImporter(
                db=self.db,
                universe=definition.universe,
                provider=provider,
            )
            importer.import_universe()
            members = provider.get_members()
            result.universes_processed += 1
            result.companies_processed += len(members)
            result.tickers.update(
                member.ticker
                for member in members
            )
        self.logger.info(
            "Universe synchronization finished. %d unique tickers.",
            len(result.tickers),
        )
        return result
