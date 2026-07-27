from models.universe import Universe
from db.database import Database


class UniverseRepository:

    def __init__(self, db: Database):
        self.db = db

    def get_by_code(self, code: str) -> Universe | None:

        sql = """
            SELECT
                universe_id,
                code,
                name,
                provider,
                enabled,
                sort_order
            FROM core.universes
            WHERE code = %s;
        """

        row = self.db.fetch_one(sql, (code,))

        if row is None:
            return None

        return Universe(
            universe_id=row["universe_id"],
            code=row["code"],
            name=row["name"],
            provider=row["provider"],
            enabled=row["enabled"],
            sort_order=row["sort_order"],
        )

    def create(self, universe: Universe) -> Universe:

        sql = """
            INSERT INTO core.universes
            (
                code,
                name,
                provider,
                enabled,
                sort_order
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING universe_id;
        """

        row = self.db.fetch_one(
            sql,
            (
                universe.code,
                universe.name,
                universe.provider,
                universe.enabled,
                universe.sort_order,
            ),
        )

        if row is None:
            raise RuntimeError("Failed to create universe.")
        universe.universe_id = row["universe_id"]
        return universe

    def get_or_create(self, universe: Universe) -> Universe:
        existing = self.get_by_code(universe.code)
        if existing is not None:
            return existing
        return self.create(universe)
