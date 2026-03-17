"""MySQL connector — requires ``datadex[mysql]`` (pymysql)."""

from __future__ import annotations

from typing import Any

from datadex.connectors.base import BaseConnector

_INSTALL_MSG = "MySQL connector requires pymysql: pip install datadex[mysql]"


class MySQLConnector(BaseConnector):
    """Read and write data from a MySQL / MariaDB database.

    Parameters
    ----------
    host:
        Database host.
    port:
        Database port (default: 3306).
    database:
        Database / schema name.
    user:
        Database user.
    password:
        Database password.
    table:
        Default table name for reads/writes.
    """

    name: str = "mysql"

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        *,
        port: int = 3306,
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
        """Open a pymysql connection."""
        try:
            import pymysql  # noqa: PLC0415
            import pymysql.cursors  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(_INSTALL_MSG) from exc

        self._conn = pymysql.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password,
            cursorclass=pymysql.cursors.DictCursor,
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
            return list(cur.fetchall())

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
        col_names = ", ".join(f"`{c}`" for c in cols)
        sql = f"INSERT INTO `{target}` ({col_names}) VALUES ({placeholders})"  # noqa: S608

        with self._conn.cursor() as cur:
            for row in data:
                cur.execute(sql, [row[c] for c in cols])
        self._conn.commit()
        return len(data)

    def close(self) -> None:
        """Close the pymysql connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def health_check(self) -> bool:
        """Ping the database."""
        if self._conn is None:
            return False
        try:
            self._conn.ping(reconnect=False)
            return True
        except Exception:  # noqa: BLE001
            return False
