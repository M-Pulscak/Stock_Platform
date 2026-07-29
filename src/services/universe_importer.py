from db.database import Database
from models.universe import Universe
from providers.universe.universe_provider import UniverseProvider
from repositories.universe_member_repository import UniverseMemberRepository
from repositories.universe_repository import UniverseRepository
from utils.logger import get_logger


class UniverseImporter:

    def __init__(
        self,
        db: Database,
        universe: Universe,
        provider: UniverseProvider,
    ):
        self.db = db
        self.universe = universe
        self.provider = provider
        self.universe_repo = UniverseRepository(db)
        self.member_repo = UniverseMemberRepository(db)
        self.logger = get_logger("UniverseImporter")

    def import_universe(self) -> Universe:
        self.logger.info(" ")
        self.logger.info(
            "Import členů indexu %s (%s)",
            self.universe.code,
            self.universe.provider,
        )
        self.logger.info("-" * 60)
        universe = self.universe_repo.get_or_create(self.universe)
        if universe.universe_id is None:
            raise RuntimeError("Universe ID was not assigned.")
        self.logger.info("Downloading členů indexu...")
        members = self.provider.get_members()
        self.logger.info("Načteno %d členů.", len(members))
        self.logger.info("Synchronizace databáze...")
        self.member_repo.replace_members(
            universe.universe_id,
            members,
        )
        self.logger.info(
            "Tickery v indexu %s aktualizovány (%d členů).",
            universe.code,
            len(members),
        )
        return universe
