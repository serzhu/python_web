import psycopg2
from contextlib import contextmanager


@contextmanager
def create_connection():
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'test', user = 'postgres', password = '7456')
        yield conn
        conn.close()
    except psycopg2.OperationalError as err:
        raise RuntimeError('Failed to create db {err}')

