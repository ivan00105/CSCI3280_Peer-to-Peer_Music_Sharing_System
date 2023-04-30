import sqlite3
from timeit import default_timer


class SqliteDB(object):
    db_path = 'songs.db'

    def __init__(self, commit=True, log_time=False, log_label='"elapsed time', dict_format=True):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        self._sql = self.db_path
        self._dict_format = dict_format

    def __enter__(self):
        if self._log_time:
            self._start = default_timer()

        conn = sqlite3.connect(self._sql)

        if self._dict_format:
            conn.row_factory = self._dict_factory

        cursor = conn.cursor()
        self._conn = conn
        self._cursor = cursor
        return self

    @staticmethod
    def _dict_factory(_cursor, row):
        return {col[0]: row[index] for index, col in enumerate(_cursor.description)}

    def __exit__(self, *exc_info):
        if self._commit:
            self._conn.commit()

        self._cursor.close()
        self._conn.close()

        if self._log_time:
            diff = default_timer() - self._start
            print('-- %s: %.6f sec' % (self._log_label, diff))

    def execute_query(self, sql, params=None):
        if params:
            if not isinstance(params, tuple):
                params = (params,)
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor

    def fetch_one(self, sql, params=None):
        self.execute_query(sql, params)
        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):
        self.execute_query(sql, params)
        return self.cursor.fetchall()

    @property
    def cursor(self):
        return self._cursor
