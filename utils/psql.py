import os
import psycopg2
import psycopg2.extras
from psycopg2 import sql

from conf.config import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT
from .log import LOG

class PSQL:

    _CONNECTION = None

    staticmethod
    def get_DB_connection():
        if not PSQL._CONNECTION:
            try:
                conn = psycopg2.connect(
                    host=DB_HOST,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS,
                    port=DB_PORT)
                conn.autocommit = True
                PSQL._CONNECTION = conn
                return PSQL._CONNECTION
            except (psycopg2.OperationalError, KeyError):
                LOG.error("Failed to connect to DB")
                exit(1)
        else:
            return PSQL._CONNECTION

    staticmethod
    def get_sql_transaction_from_file(script_path=None):
        transaction = None
        try:
            with open(script_path, mode='r') as f:
                transaction = f.read()
        except Exception:
            LOG.error('Unable to open the script file')
            raise

        try:
            transaction = sql.SQL(string=transaction)
        except Exception:
            LOG.error(f"Failed to validate the transaction for the script '{script_path}'")
            raise
        return transaction

    staticmethod
    def get_results(cursor, transaction, attributes_tuple=None):
        try:
            if not attributes_tuple:
                cursor.execute(transaction)
            else:
                cursor.execute(transaction, attributes_tuple)
            return cursor.fetchall()
        except psycopg2.ProgrammingError as ex_pr:
            LOG.info(f"No data found in DB for transaction: '{transaction}' and attributes: {attributes_tuple}. Exception: {ex_pr}") 
            return tuple()
        except Exception as ex:
            LOG.error(f"There was an error: {ex}")
            return tuple()
