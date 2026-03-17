"""PostgreSQL connector — requires ``datadex[postgres]`` (psycopg[binary])."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_INSTALL_MSG = "PostgreSQL connector requires psycopg: pip install datadex[postgres]"


class PostgresConnector(BaseConnector):
    """Read and write data from a PostgreSQL database.

    Parameters
    ----------
    host:
        Database host.
    port:
        Database port (default: 5432).
    database:
        Database name.
    user:
        Database user.
    password:
        Database password.
    table:
        Default table name for reads/writes.
    """

    name: str = "postgres"

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        *,
        port: int = 5432,
        table: str = "",
    ) -> None:
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password
        self._table = table
        self._conn: Any = None

    def connect(self) -> None:
        """Open a psycopg connection."""
        try:
            import psycopg  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(_INSTALL_MSG) from exc

        self._conn = psycopg.connect(
            host=self._host,
            port=self._port,
            dbname=self._database,
            user=self._user,
            password=self._password,
        )

    def read(self, query: str = "", table: str = "", **kwargs: Any) -> list[dict[str, Any]]:
        """Execute a SELECT query and return rows as dicts.

        Parameters
        ----------
        query:
            Raw SQL query.  Takes precedence over *table*.
        table:
            Table name to ``SELECT * FROM``.  Falls back to ``self._table``.
        """
        if self._conn is None:
            raise RuntimeError("Call connect() before read()")

        sql = query or f"SELECT * FROM {table or self._table}"  # noqa: S608
        with self._conn.cursor() as cur:
            cur.execute(sql)
            cols = [desc[0] for desc in cur.description]
            return [dict(zip(cols, row, strict=True)) for row in cur.fetchall()]

    def write(self, data: list[dict[str, Any]], table: str = "", **kwargs: Any) -> int:
        """Insert rows into *table* using parameterised queries.

        Parameters
        ----------
        data:
            List of row dicts to insert.
        table:
            Target table.  Falls back to ``self._table``.
        """
        if not data:
            return 0
        if self._conn is None:
            raise RuntimeError("Call connect() before write()")

        target = table or self._table
        if not target:
            raise ValueError("Specify a target table via the table parameter or constructor")

        cols = list(data[0].keys())
        placeholders = ", ".join(["%s"] * len(cols))
        col_names = ", ".join(cols)
        sql = f"INSERT INTO {target} ({col_names}) VALUES ({placeholders})"  # noqa: S608

        with self._conn.cursor() as cur:
            for row in data:
                cur.execute(sql, [row[c] for c in cols])
        self._conn.commit()
        return len(data)

    def close(self) -> None:
        """Close the psycopg connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def health_check(self) -> bool:
        """Ping the database with a trivial query."""
        if self._conn is None:
            return False
        try:
            with self._conn.cursor() as cur:
                cur.execute("SELECT 1")
            return True
        except Exception:  # noqa: BLE001
            return False
