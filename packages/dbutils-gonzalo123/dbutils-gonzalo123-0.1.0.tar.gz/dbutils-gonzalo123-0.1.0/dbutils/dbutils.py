from contextlib import contextmanager

import psycopg2
from psycopg2 import sql as psycopg2_sql
from psycopg2.extras import NamedTupleConnection, NamedTupleCursor, execute_batch


def _get_conditions(where):
    return [psycopg2_sql.SQL("{identifier} = {placeholder}").format(
        identifier=psycopg2_sql.Identifier(key),
        placeholder=psycopg2_sql.Placeholder(key)) for key in where]


@contextmanager
def transactional_cursor(conn, named_tuple=False):
    try:
        with conn as connection:
            with get_cursor(conn=connection, named_tuple=named_tuple) as cursor:
                yield cursor
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


@contextmanager
def transactional(conn, named_tuple=False):
    try:
        with conn as connection:
            with get_cursor(conn=connection, named_tuple=named_tuple) as cursor:
                yield Db(cursor)
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def get_conn(dsn, named_tuple=False, autocommit=False):
    conn = psycopg2.connect(
        dsn=dsn,
        connection_factory=NamedTupleConnection if named_tuple else None,
    )
    conn.autocommit = autocommit

    return conn


def get_cursor(conn, named_tuple=True):
    return conn.cursor(cursor_factory=NamedTupleCursor if named_tuple else None)


def fetch_all(cursor, sql, params=None):
    params = {} if params is None else params
    cursor.execute(sql, params)
    return cursor.fetchall()


def fetch_one(cursor, sql, where=None):
    where = {} if where is None else where
    cursor.execute(sql, where)
    data = cursor.fetchone()

    return data[0]


def sp_fetch_all(cursor, function, params=None):
    params = {} if params is None else params
    cursor.callproc(function, params)

    return cursor.fetchall()


def sp_fetch_one(cursor, function, params=None):
    params = {} if params is None else params
    cursor.callproc(function, params)
    data = cursor.fetchone()

    return data[0]


def _get_insert_sql(table, values):
    keys = values[0].keys() if type(values) is list else values.keys()

    raw_sql = "insert into {tbl} ({t_fields}) values ({t_values})"
    return psycopg2_sql.SQL(raw_sql).format(
        tbl=psycopg2_sql.Identifier(table),
        t_fields=psycopg2_sql.SQL(', ').join(map(psycopg2_sql.Identifier, keys)),
        t_values=psycopg2_sql.SQL(', ').join(map(psycopg2_sql.Placeholder, keys)))


def insert(cursor, table, values):
    sql = _get_insert_sql(table=table, values=values)
    cursor.executemany(sql, values) if type(values) is list else cursor.execute(sql, values)

    return cursor.rowcount


def insert_batch(cursor, table, values):
    sql = _get_insert_sql(table=table, values=values)
    execute_batch(cur=cursor, sql=sql, argslist=values)

    return cursor.rowcount


def delete(cursor, table, where=None):
    if where:
        raw_sql = "delete from {tbl} where {t_where}"
    else:
        raw_sql = "delete from {tbl}"
        where = {}

    sql = psycopg2_sql.SQL(raw_sql).format(
        tbl=psycopg2_sql.Identifier(table),
        t_where=psycopg2_sql.SQL(' and ').join(_get_conditions(where)))

    cursor.execute(sql, where)

    return cursor.rowcount


def update(cursor, table, data, identifier):
    raw_sql = "update {tbl} set {t_set} where {t_where}"

    sql = psycopg2_sql.SQL(raw_sql).format(
        tbl=psycopg2_sql.Identifier(table),
        t_set=psycopg2_sql.SQL(', ').join(_get_conditions(data)),
        t_where=psycopg2_sql.SQL(' and ').join(_get_conditions(identifier)))

    cursor.execute(sql, {**data, **identifier})

    return cursor.rowcount


def upsert(cursor, table, data, identifier):
    raw_sql = """
        WITH 
            upsert AS (
                UPDATE {tbl} 
                SET {t_set}
                WHERE {t_where}
                RETURNING {tbl}.*),
            inserted AS (
                INSERT INTO {tbl} ({t_fields})
                SELECT {t_select_fields}
                WHERE NOT EXISTS (SELECT 1 FROM upsert)
                RETURNING *)
        SELECT * FROM upsert 
        UNION ALL 
        SELECT * FROM inserted
    """

    merger_data = {**data, **identifier}
    sql = psycopg2_sql.SQL(raw_sql).format(
        tbl=psycopg2_sql.Identifier(table),
        t_set=psycopg2_sql.SQL(', ').join(_get_conditions(data)),
        t_where=psycopg2_sql.SQL(' and ').join(_get_conditions(identifier)),
        t_fields=psycopg2_sql.SQL(', ').join(map(psycopg2_sql.Identifier, merger_data.keys())),
        t_select_fields=psycopg2_sql.SQL(', ').join(map(psycopg2_sql.Placeholder, merger_data.keys())))

    cursor.execute(sql, merger_data)
    return cursor.rowcount


class Db:
    def __init__(self, cursor):
        self.cursor = cursor

    def fetch_all(self, sql, params=None):
        return fetch_all(self.cursor, sql, params)

    def upsert(self, table, data, identifier):
        return upsert(self.cursor, table, data, identifier)

    def update(self, table, data, identifier):
        return update(self.cursor, table, data, identifier)

    def delete(self, table, where=None):
        return delete(self.cursor, table, where)

    def insert(self, table, values):
        return insert(self.cursor, table, values)

    def insert_batch(self, table, values):
        return insert_batch(self.cursor, table, values)

    def sp_fetch_one(self, function, params=None):
        return sp_fetch_one(self.cursor, function, params)

    def sp_fetch_all(self, function, params=None):
        return sp_fetch_all(self.cursor, function, params)

    def fetch_one(self, sql, where=None):
        return fetch_one(self.cursor, sql, where)

    def get_cursor(self):
        return self.cursor
