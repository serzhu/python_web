from psycopg2 import DatabaseError
import logging
from connect import create_connection


def create_table(conn, sql_expression:str):
    c = conn.cursor()
    try:
        c.execute(sql_expression)
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
     id SERIAL PRIMARY KEY,
     name VARCHAR(120),
     email VARCHAR(120),
     password VARCHAR(120),
     age SMALLINT CHECK(age > 18 AND age < 75),
    );
    """
    try:
        with create_connection() as conn:
            if conn is not None:
                # create projects table
                create_table(conn, sql_create_users_table)
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as err:
        logging.error(err)