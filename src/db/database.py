from __future__ import annotations
from collections.abc import Sequence
from types import TracebackType
from typing import Any, Mapping, TypeAlias, cast
import psycopg
from psycopg import Connection
from psycopg.rows import dict_row
from typing_extensions import LiteralString
from config import DATABASE


# ----------------------------------------------------------------------
# Shared type aliases
# ----------------------------------------------------------------------

Sql: TypeAlias = str
SqlParams: TypeAlias = tuple[Any, ...] | None
RowsParams: TypeAlias = list[tuple[Any, ...]]
Row: TypeAlias = Mapping[str, Any]


class Database:
    """
    Lightweight PostgreSQL wrapper.
    """

    def __init__(self) -> None:
        self._conn: Connection[Any] | None = None

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------
    def __enter__(self) -> Database:

        self._conn = psycopg.connect(
            host=DATABASE.host,
            port=DATABASE.port,
            dbname=DATABASE.name,
            user=DATABASE.user,
            password=DATABASE.password,
            sslmode="require",
            connect_timeout=10,
        )

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc_value: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:

        if self._conn is None:
            return

        try:
            if exc_type is None:
                self._conn.commit()
            else:
                self._conn.rollback()
        finally:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def is_connected(self) -> bool:
        return self._conn is not None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _connection(self) -> Connection[Any]:

        if self._conn is None:
            raise RuntimeError("Database connection is not open.")

        return self._conn

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------
    def execute(
        self,
        sql: Sql,
        params: SqlParams = None,
    ) -> None:

        with self._connection().cursor(row_factory=dict_row) as cur:
            cur.execute(cast(LiteralString, sql), params)

    def execute_returning(
        self,
        sql: Sql,
        params: SqlParams = None,
    ) -> Row | None:

        with self._connection().cursor(row_factory=dict_row) as cur:
            cur.execute(cast(LiteralString, sql), params)
            return cur.fetchone()

    def execute_many(
        self,
        sql: Sql,
        params: RowsParams,
    ) -> None:

        with self._connection().cursor(row_factory=dict_row) as cur:
            cur.executemany(cast(LiteralString, sql), params)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def fetch_one(
        self,
        sql: Sql,
        params: SqlParams = None,
    ) -> Row | None:

        with self._connection().cursor(row_factory=dict_row) as cur:
            cur.execute(cast(LiteralString, sql), params)
            return cur.fetchone()

    def fetch_all(
        self,
        sql: Sql,
        params: SqlParams = None,
    ) -> Sequence[Row]:

        with self._connection().cursor(row_factory=dict_row) as cur:
            cur.execute(cast(LiteralString, sql), params)
            return cur.fetchall()

    def scalar(
        self,
        sql: Sql,
        params: SqlParams = None,
    ) -> Any:
        row = self.fetch_one(sql, params)
        if row is None:
            return None
        return next(iter(row.values()))
