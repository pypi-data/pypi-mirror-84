import prestodb


class PrestoClient(object):
    def __init__(self, host, port, user, catalog, schema):
        self._host = host
        self._port = port
        self._user = user
        self._catalog = catalog
        self._schema = schema
        self._conn = None
        self._cursor = None

    def __enter__(self):
        self._conn = prestodb.dbapi.connect(host=self._host, port=self._port, user=self._user, catalog=self._catalog,
                                            schema=self._schema)
        self._cursor = self._conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()
        self._conn.close()

    @property
    def conn(self):
        return self._conn

    def query_all(self, sql):
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()
        self._conn.close()

