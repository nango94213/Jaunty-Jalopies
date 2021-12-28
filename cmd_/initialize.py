import os
import psycopg2
import psycopg2.extras

from conf.config import RESET_DB, SOURCE_DATA
from utils import LOG, PSQL
from .populate_db import add_known_users, populate_db
from demo_data.etl import ETL

def reset_db():
    LOG.info("Initializing DB...")

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

        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_drop_tables)
                cur.execute(sql_create_tables)
        
        add_known_users()

        if SOURCE_DATA == 'demo_data':
            ETL.ingest_data_from_demo_data()
        else:
            populate_db(conn)

    else:
        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_create_tables)