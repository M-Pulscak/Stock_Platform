from db.database import Database
from models.universe_member import UniverseMember


class UniverseMemberRepository:

    def __init__(self, db: Database):
        self.db = db

    def get_members(self, universe_id: int) -> list[UniverseMember]:

        sql = """
            SELECT
                ticker,
                company_name,
                sector,
                industry
            FROM core.universe_members
            WHERE universe_id = %s
            ORDER BY ticker;
        """

        rows = self.db.fetch_all(sql, (universe_id,))

        return [
            UniverseMember(
                ticker=row["ticker"],
                company_name=row["company_name"],
                sector=row["sector"],
                industry=row["industry"],
            )
            for row in rows
        ]

    def delete_by_universe(self, universe_id: int) -> None:

        sql = """
            DELETE
            FROM core.universe_members
            WHERE universe_id = %s;
        """

        self.db.execute(sql, (universe_id,))

    def insert_many(
        self,
        universe_id: int,
        members: list[UniverseMember],
    ) -> None:

        if not members:
            return

        sql = """
            INSERT INTO core.universe_members
            (
                universe_id,
                ticker,
                company_name,
                sector,
                industry
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            );
        """

        rows = [
            (
                universe_id,
                member.ticker,
                member.company_name,
                member.sector,
                member.industry,
            )
            for member in members
        ]

        self.db.execute_many(sql, rows)

    def replace_members(
        self,
        universe_id: int,
        members: list[UniverseMember],
    ) -> None:

        self.delete_by_universe(universe_id)
        self.insert_many(universe_id, members)
