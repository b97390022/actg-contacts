from __future__ import annotations

from ldap3 import ALL, Connection, Server
from ldap3.abstract.entry import Entry


class LDAPServer:

    def __init__(self,
                 host: str,
                 port: int | None = None,
                 user: str | None = None,
                 password: str | None = None) -> None:
        self._server = Server(host, port, get_info=ALL)
        self._user = user
        self._password = password

    def search(self, *args, **kwargs) -> list[Entry]:
        with Connection(self._server, self._user, self._password) as conn:
            conn.search(*args, **kwargs)
            return conn.entries
