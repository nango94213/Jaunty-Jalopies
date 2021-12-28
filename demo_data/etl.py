import os
from datetime import datetime

import unicodecsv

from utils import LOG, PSQL, Hasher
from sql_.sequel import SEQUEL


# TODO: Dry this code, done in a rush
class ETL:

    @staticmethod
    def transform_date(date_):
        """
        This method will take a date with format: 3/2/2021
        and transform it into 2021-03-02
        """
        return datetime.strptime(date_, '%m/%d/%Y').strftime('%Y-%m-%d')

    @staticmethod
    def etl_users():
        FIELD_NAMES = ['username', 'password', 'u_f_name', 'u_l_name', 'roles']		
        file_path = 'demo_data/data/users.tsv'		
        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='rb') as tsv_file:
                    reader = unicodecsv.DictReader(
                        csvfile=tsv_file,
                        fieldnames=FIELD_NAMES,
                        delimiter="\t",
                        encoding='utf-8-sig'
                    )
                
                    # Ignore headers
                    headers = next(reader)
                    
                    for row in reader:
                        role = 'owner' if 'owner' in row['roles'] else row['roles']
                        transaction = SEQUEL.INSERT_PRIVILEGED_USER.format(
                            username=row['username'],
                            password=Hasher.hash_pass(row['password']),
                            firstname=row['u_f_name'],
                            lastname=row['u_l_name'],
                            role=role
                        )
                        cur.execute(transaction)
                        
                        insert_statement = f"INSERT_{role.upper()}"
                        transaction = getattr(SEQUEL, insert_statement).format(
                            username=row['username']
                        )
                        cur.execute(transaction)

    @staticmethod
    def etl_customers():

        FIELD_NAMES_BUSINESS = [
            'tax_num', 'bzn_name', 'c_f_name', 'c_l_name', 'c_title', 'email', 
            'phone', 'cst_street_addr', 'cst_city', 'cst_state', 'cst_postal_code']		
        file_path_business = 'demo_data/data/business.tsv'	

        FIELD_NAMES_INDIVIDUAL = [
            'driver_lic', 'p_f_name', 'p_l_name', 'email', 'phone', 'cst_street_addr', 
            'cst_city', 'cst_state', 'cst_postal_code']		
        file_path_individual = 'demo_data/data/person.tsv'	

        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path_business, mode='rb') as tsv_file:
                    reader = unicodecsv.DictReader(
                        csvfile=tsv_file,
                        fieldnames=FIELD_NAMES_BUSINESS,
                        delimiter="\t",
                        encoding='utf-8-sig'
                    )
                
                    # Ignore headers
                    headers = next(reader)

                    for row in reader:
                        transaction = SEQUEL.INSERT_DATA_BUSINESS.format(
                            id=row['tax_num'],
                            address=f"{row['cst_street_addr']}, {row['cst_city']}, {row['cst_state']} {row['cst_postal_code']}",
                            phone_number=row['phone'],
                            email_address=row['email'],
                            tin=row['tax_num'],
                            business_name=row['bzn_name'],
                            primary_contact_name=f"{row['c_f_name']} {row['c_l_name']}",
                            primary_contact_title=row['c_title']
                        )
                        cur.execute(transaction)

                with open(file_path_individual, mode='rb') as tsv_file:
                    reader = unicodecsv.DictReader(
                        csvfile=tsv_file,
                        fieldnames=FIELD_NAMES_INDIVIDUAL,
                        delimiter="\t",
                        encoding='utf-8-sig'
                    )
                
                    # Ignore headers
                    headers = next(reader)

                    for row in reader:
                        transaction = SEQUEL.INSERT_DATA_INDIVIDUAL.format(
                            id=row['driver_lic'],
                            address=f"{row['cst_street_addr']}, {row['cst_city']}, {row['cst_state']} {row['cst_postal_code']}",
                            phone_number=row['phone'],
                            email_address=row['email'],
                            driver_license_number=row['driver_lic'],
                            firstname=row['p_f_name'],
                            lastname=row['p_l_name']
                        )
                        cur.execute(transaction)

    @staticmethod
    def etl_vehicles():

        FIELD_NAMES = [
            # All Vehicles
            'VIN', 'year', 'manufacturer_name', 'model', 'Colors', 'description', 
            'invoice_price', 'added_by', 'date_added', 'vehicle_type', 
            # Car
            'number_doors',
            # Convertible
            'back_seat_count', 'roof_type',
            # SUV
            'num_cupholders', 'drive_train_type',
            # Truck
            'num_rear_axles', 'cover_type', 'capacity',
            # Van
            'driver_side_door',
            # Sold Vehicles
            'sold_by', 'sale_date', 'sold_price', 'customer'
            ]
        file_path = 'demo_data/data/vehicles.tsv'	

        sql_transaction_per_vehicle_type = {
            "SUV": SEQUEL.INSERT_DATA_SUV,
            "Convertible": SEQUEL.INSERT_DATA_CONVERTIBLE,
            "Car": SEQUEL.INSERT_DATA_CAR,
            "Van": SEQUEL.INSERT_DATA_VAN,
            "Truck": SEQUEL.INSERT_DATA_TRUCK
        }

        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='rb') as tsv_file:
                    reader = unicodecsv.DictReader(
                        csvfile=tsv_file,
                        fieldnames=FIELD_NAMES,
                        delimiter="\t",
                        encoding='utf-8-sig'
                    )
                
                    # Ignore headers
                    headers = next(reader)

                    for row in reader:
                        # Add Vehicle, Specifics and Colors
                        insert_statement_colors = ""
                        for color in [color.strip() for color in row['Colors'].split(",")] if len(row['Colors']) > 1 else [row['Colors']]:
                            insert_statement_colors += f"""INSERT INTO Vehicle_Color VALUES ('{row["VIN"]}', '{color}');"""
                        

                        transaction = sql_transaction_per_vehicle_type[row['vehicle_type']].format(
                            # All vehicles
                            vin=row['VIN'],
                            description=row['description'].replace(";",","),
                            invoice_price=row['invoice_price'],
                            type=row['vehicle_type'],
                            model_year=row['year'],
                            model_name=row['model'],
                            date_added=ETL.transform_date(row['date_added']),
                            clerk_username=row['added_by'],
                            manufacturer_name=row['manufacturer_name'],
                            # SUV
                            number_of_cup_holders=row['num_cupholders'],
                            drivetrain_type=row['drive_train_type'],
                            # Van
                            has_driver_side_backdoor=True if row['driver_side_door'] == '1' else False,
                            # Truck
                            cargo_capacity=row['capacity'],
                            cargo_cover_type=row['cover_type'] or None,
                            no_rear_axles=row['num_rear_axles'],
                            # Convertible
                            back_seat_count=row['back_seat_count'],
                            roof_type=row['roof_type'],
                            # Car
                            number_of_doors=row['number_doors'],
                            # Colors
                            insert_statement_colors=insert_statement_colors
                        )

                        cur.execute(transaction)

                        # Add Sale if Vehicle was Sold
                        sold_by, sale_date, customer = row['sold_by'].strip(), row['sale_date'].strip(), row['customer'].strip()
                        if sold_by and sale_date and customer:
                            transaction = SEQUEL.SELL_VEHICLE.format(
                                vin=row['VIN'],
                                id=customer,
                                sales_person_username=sold_by,
                                sale_date=ETL.transform_date(sale_date),
                                sold_price=row['sold_price']
                            )
                            cur.execute(transaction)

    @staticmethod
    def add_manufacturers():
        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    PSQL.get_sql_transaction_from_file(
                        os.path.join(
                            os.path.dirname(__file__),
                            '..',
                            'sql_',
                            'insert_manufacturers.sql'
                        )))

    @staticmethod
    def etl_repairs():
        FIELD_NAMES = [
            'VIN', 'customer', 'service_writer', 'start_date', 'completion_date', 'odometer', 
            'labor_cost', 'repair_desc']
        file_path = 'demo_data/data/repairs.tsv'	

        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='rb') as tsv_file:
                    reader = unicodecsv.DictReader(
                        csvfile=tsv_file,
                        fieldnames=FIELD_NAMES,
                        delimiter="\t",
                        encoding='utf-8-sig'
                    )
                
                    # Ignore headers
                    headers = next(reader)

                    for row in reader:
                        transaction = SEQUEL.INSERT_COMPLETED_REPAIR.format(
                            vin=row['VIN'],
                            customer_id=row['customer'],
                            start_date=ETL.transform_date(row['start_date']),
                            service_writer_username=row['service_writer'],
                            repair_description=row['repair_desc'].replace(";",","),
                            completion_date=ETL.transform_date(row['completion_date']),
                            odometer_reading=row['odometer'],
                            labor_charges=row['labor_cost'])

                        cur.execute(transaction)

    @staticmethod
    def etl_parts():
        FIELD_NAMES = ['VIN', 'start_date', 'pt_number', 'vendor_name', 'quantity', 'pt_price']
        file_path = 'demo_data/data/parts.tsv'	

        with PSQL.get_DB_connection() as conn:
            with conn.cursor() as cur:
                with open(file_path, mode='rb') as tsv_file:
                    reader = unicodecsv.DictReader(
                        csvfile=tsv_file,
                        fieldnames=FIELD_NAMES,
                        delimiter="\t",
                        encoding='utf-8-sig'
                    )
                
                    # Ignore headers
                    headers = next(reader)

                    for row in reader:
                        # HACK: Our relation for Parts needs a customerId
                        # In the future we can change that, but for now, let's
                        # just get the users from repairs, and use that into the parts. 
                        # This will create an extra query not needed, but its a temp solution.
                        cur.execute(
                            f""" SELECT CustomerID FROM Repair 
                                WHERE VIN='{row['VIN']}'
                                AND startDate='{row['start_date']}';""")
                        customer_id = cur.fetchone()[0]

                        transaction = SEQUEL.INSERT_INTO_PARTS.format(
                            vin=row['VIN'],
                            start_date=ETL.transform_date(row['start_date']),
                            customer_id=customer_id,
                            part_number=row['pt_number'],
                            vendor_name=row['vendor_name'],
                            quantity=row['quantity'],
                            price=row['pt_price'])

                        cur.execute(transaction)

    @staticmethod
    def ingest_data_from_demo_data():
        ETL.etl_users()
        ETL.etl_customers()
        ETL.add_manufacturers()
        ETL.etl_vehicles()
        ETL.etl_repairs()
        ETL.etl_parts()
