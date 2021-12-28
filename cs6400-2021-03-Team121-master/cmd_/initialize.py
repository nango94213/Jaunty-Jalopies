import os
import psycopg2
import psycopg2.extras

from conf.config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, RESET_DB
from utils import LOG, PSQL
from .populate_db import populate_db

def reset_db():
    LOG.info("Initializing DB...")

    conn = PSQL.get_DB_connection()

    create_tables_script_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'sql_',
        'team121_p3_schema.sql'
    )

    sql_create_tables = PSQL.get_sql_transaction_from_file(create_tables_script_path)

    if RESET_DB:
        drop_tables_script_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'sql_',
            'drop_tables.sql'
        )
        sql_drop_tables = PSQL.get_sql_transaction_from_file(drop_tables_script_path)

        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_drop_tables)
                cur.execute(sql_create_tables)
        
        populate_db(conn)

    else:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_create_tables)