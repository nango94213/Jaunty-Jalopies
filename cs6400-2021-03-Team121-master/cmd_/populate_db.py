import os

from sql_.sequel import SEQUEL
from utils import PSQL, Hasher
from .default_values import DefaultValues

def populate_db(conn):

    # ======================================================
    # Execute transactions
    # ======================================================
    with conn:
        with conn.cursor() as cur:
            # ======================================================
            # Add Users
            # ======================================================
            for user in DefaultValues.PRIVILEGED_USERS:
                transaction = SEQUEL.INSERT_PRIVILEGED_USER.format(
                    username=user['username'],
                    password=Hasher.hash_pass(user['password']),
                    firstname=user['firstname'],
                    lastname=user['lastname'],
                    role=user['role']
                )
                cur.execute(transaction)
                
                insert_statement = f"INSERT_{user['role'].upper()}"
                transaction = getattr(SEQUEL, insert_statement).format(
                    username=user['username']
                )
                cur.execute(transaction)
                
            # ======================================================
            # Add Other Initial Data (Manufacturers, Vehicles, etc.)
            # ======================================================
            insert_data_script_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'sql_',
                'insert_most_initial_data.sql'
            )

            sql_insert_data = PSQL.get_sql_transaction_from_file(insert_data_script_path)
            cur.execute(sql_insert_data)
