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

        with self.db.connection.cursor() as cur:
            cur.execute(sql, (code,))
            row = cur.fetchone()

        if row is None:
            return None

        return Universe(
            universe_id=row[0],
            code=row[1],
            name=row[2],
            provider=row[3],
            enabled=row[4],
            sort_order=row[5]
        )
