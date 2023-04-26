import sqlite3
from timeit import default_timer


class SqliteDB(object):

    db_path = 'songs.db'
    def __init__(self, commit=True, log_time=False, log_label='"elapsed time', dict_formate=True):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label
        self._sql = self.db_path
        self._dict_formate = dict_formate

    def __enter__(self):
        def dict_factory(_cursor, row):
            d = {}
            for index, col in enumerate(_cursor.description):
                d[col[0]] = row[index]
            return d

        if self._log_time is True:
            self._start = default_timer()
        conn = sqlite3.connect(self._sql)
        if self._dict_formate:
            conn.row_factory = dict_factory
        cursor = conn.cursor()
        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        if self._commit:
            self._conn.commit()
        self._cursor.close()
        self._conn.close()
        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f sec' % (self._log_label, diff))

    def fetch_one(self, sql, params=()):
        if params is None:
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        if not type(params) is tuple:
            params = (params,)  # 转换为元组
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def fetch_all(self, sql, params=None):
        if params is None:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        if not type(params) is tuple:
            params = (params,)  # 转换为元组
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    @property
    def cursor(self):
        return self._cursor
