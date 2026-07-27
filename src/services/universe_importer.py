from db.database import Database
from models.universe import Universe
from providers.universe.universe_provider import UniverseProvider
from repositories.universe_member_repository import UniverseMemberRepository
from repositories.universe_repository import UniverseRepository


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

    def import_universe(self) -> Universe:

        # vytvoří univerzum, pokud ještě neexistuje
        universe = self.universe_repo.get_or_create(self.universe)

        if universe.universe_id is None:
            raise RuntimeError("Universe ID was not assigned.")

        # načte aktuální členy od providera
        members = self.provider.get_members()

        # kompletně nahradí obsah univerza
        self.member_repo.replace_members(
            universe.universe_id,
            members,
        )

        return universe
