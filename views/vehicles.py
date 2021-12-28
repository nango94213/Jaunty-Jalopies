from datetime import datetime

from flask import request, render_template, session, redirect, flash
import psycopg2

from views.base import Base 
from cmd_.default_values import DefaultValues
from sql_.sequel import SEQUEL
from utils import PSQL
from utils.utilities import is_valid

class Vehicle(Base):

    def __init__(self, **kwargs):
        super(Vehicle, self).__init__(**kwargs)

    def get_details(self, vin=None):
        """
        To display single items
        """
        self.refresh_data()

        if request.method == 'GET':

            if not vin:
                return render_template(
                    'errorPage.html',
                    error_msg="Page not found."
                )

            query = SEQUEL.SELECT_VEHICLE_BULK_DETAIL_INFO.format(
                vin=vin
            )
            vehicle = dict()
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(query)
                    vehicles = cur.fetchall()
                    if not vehicles:
                        return render_template(
                            'errorPage.html',
                            error_msg="Vehicle not found."
                        )
                    for item in vehicles:
                        if not vehicle:
                            vehicle = {
                                'vin': vin,
                                "type": item['type'],
                                "attrs": dict(),
                                "model_year": item['year'],
                                "manufacturer": item['mfname'],
                                "model_name": item['mname'],
                                "inventory_clerk": item['inventory_clerk_name'],
                                "date_added": item['dateadded'],
                                "colors": item['color'],
                                "description": item["description"],
                                "invoice_price": "$ {:.2f}".format(float(item['invoiceprice'])),
                                "list_price": "$ {:.2f}".format(float(item['listprice']))
                            }
                        else:
                            if item['color'] not in vehicle['colors']:
                                vehicle['colors'] += f",{item['color']}"

                    query_vehicle_attributes = SEQUEL.SELECT_ATTRIBUTES_FROM_VEHICLE_TYPE.format(
                        vehicle_type=vehicle['type'],
                        vin=vin
                    )
                    cur.execute(query_vehicle_attributes)
                    vehicle_attributes = cur.fetchone()
                    
                    for attribute, value in vehicle_attributes.items():
                        if attribute not in ["vin"]:
                            vehicle["attrs"][attribute] = value

                    cur.execute(SEQUEL.SELECT_VEHICLE_SALE_DETAILS.format(vin=vin))
                    sale_details = cur.fetchone()

                    if sale_details:
                        vehicle['sold'] = True
                        vehicle['buyer_info'] = sale_details['customer_contact_info']
                        vehicle['sold_price'] = "$ {:.2f}".format(float(sale_details['soldprice']))
                        vehicle['sale_date'] = sale_details['saledate']
                        vehicle['sale_person'] = sale_details['sales_person_name']

                    cur.execute(SEQUEL.SELECT_REPAIRS_DETAILS.format(vin=vin))
                    repairs_details = cur.fetchone()

                    parts_total = repairs_details['parts_total'] if repairs_details and 'parts_total' in repairs_details else 0
                    if repairs_details:
                        vehicle['repaired'] = True
                        vehicle['customer_name'] = repairs_details['customer_name']
                        vehicle['service_writer'] = repairs_details['service_writer_name']
                        vehicle['repair_start_date'] = repairs_details['startdate']
                        vehicle['repair_end_date'] = repairs_details['completiondate']
                        vehicle['labor_charges'] = "$ {:.2f}".format(repairs_details['laborcharges']) if repairs_details['laborcharges'] else 'In Progress'
                        vehicle['parts_cost'] = "$ {:.2f}".format(parts_total)
                        labor_charges = float(repairs_details['laborcharges']) if repairs_details['laborcharges'] else 0
                        vehicle['total_cost'] = "$ {:.2f}".format(float(parts_total) + labor_charges)
                        vehicle['colored_class'] = "text-danger" if vehicle['labor_charges'] == "In Progress" and vehicle['repair_end_date'] == "In Progress" else ""

            return render_template(
                'detailPage.html',
                vehicle=vehicle
            )

        else:
            return render_template(
                'errorPage.html',
                error_msg="Method not allowed."
            )

    def add_new(self):

        self.refresh_data()

        if request.method == 'GET':
            return render_template(
                'newVehicleForm.html',
                entered_values=dict(),
                data=self.data
            )
        elif request.method == 'POST':

            # Get data submitted all vehicles
            vin = request.form.get("vinInputText1")
            description = request.form.get("descriptionInputText1", '')
            vehicle_type = request.form.get("vehicleTypeSelect1")
            model_year = request.form.get("yearInputText1")
            model_name = request.form.get("modelNInputText1")
            colors = request.form.get("colorsTextBox")
            manufacturer = request.form.get("manufacturerSelect1")
            invoice_price = request.form.get("invoicePInputText1")
            date_added = datetime.now().strftime('%Y-%m-%d')
            clerk_username = session['user_info']['username']

            # Get data specific to vehicle type
            # SUV
            number_of_cup_holders = request.form.get('numberOfCupholdersTypeSelect1')
            drivetrain_type = request.form.get('driveTrainTypeSelect1')

            # Convertible
            back_seat_count = request.form.get('backSeatCountTypeSelect1')
            roof_type = request.form.get('roofTypeSelect1')

            # Car
            number_of_doors = request.form.get('numberDoorsSelect1')

            # Van
            has_driver_side_backdoor = True if request.form.get('hasDriverSideDoor') else False
            
            # Truck
            cargo_capacity = request.form.get('cargoCapInputText1')
            cargo_cover_type = request.form.get('cargoCoverTypeSelect1')
            no_rear_axles = request.form.get('noRearAxlesSelect1')

            # Capture all entered data to display back if necessary (if errors)
            entered_data = {
                'vin': vin,
                'description': description,
                'invoice_price': invoice_price,
                'vehicle_type': vehicle_type,
                'model_year': model_year,
                'model_name': model_name,
                'colors': colors,
                'manufacturer': manufacturer,
                'cargo_capacity': cargo_capacity
            }

            # Validate input
            # Validate against no values submitted
            errors = dict()
            if not vin:
                errors["errors_vin"] = 'This ^^^ field is required.'
            # if not description:
            #     errors["errors_description"] = 'This ^^^ field is required.'
            if not invoice_price:
                errors["errors_invoice_price"] = 'This ^^^ field is required.'
            if not vehicle_type:
                errors["errors_vehicle_type"] = 'This ^^^ field is required.'
            if not model_year:
                errors["errors_model_year"] = 'This ^^^ field is required.'
            if not model_name:
                errors["errors_model_name"] = 'This ^^^ field is required.'
            if not colors:
                errors["errors_colors"] = 'This ^^^ field is required.'
            else:
                colors = [color.strip() for color in colors.split(",")] if len(colors) > 1 else [colors]
            if not manufacturer:
                errors["errors_manufacturer"] = 'This ^^^ field is required.'   
            if vehicle_type == "Truck" and not cargo_capacity:
                errors["errors_cargo_capacity"] = 'Cargo Capacity is a required field for trucks.'

            # Protect vs length constraints and enforce vin length
            if vin and len(vin) != 17:
                errors['errors_vin'] = "VIN number has to be 17 chars long."
            if len(description) > 200:
                errors['errors_description'] = "Description ^^^ is too long. It has to be 200 chars max."
            if len(vehicle_type) > 20:
                errors['errors_vehicle_type'] = "Type ^^^ is too long. It has to be 20 chars max."
            if len(model_name) > 50:
                errors['errors_model_name'] = "Model Name ^^^ is too long. It has to be 30 chars max."
            for color in colors:
                if len(color) > 20:
                    errors['errors_colors'] = f"Color '{color}'' ^^^ is too long. It has to be 20 chars max."
            if vehicle_type == "Truck" and len(cargo_capacity) > 20:
                errors['cargo_capacity'] = f"Cargo capacity '{cargo_capacity}' is invalid, it is too long. It has to be 20 chars max."

            # Validate specifics and repel SQL Injection
            if not is_valid("alphanumeric_or_empty_string", vin)[0]:
                errors["errors_vin"] = f"{vin} is not a valid VIN. It should not have spaces nor special chars. Only letters and numbers."
            if not is_valid("alphanumeric_spaces_dots_commas_or_empty_string", description)[0]:
                errors["errors_description"] = "Description not valid. It cannot contain special characters."
            if not is_valid("positive_decimal_or_empty_string", invoice_price)[0]:
                errors["errors_invoice_price"] = f"Invoice price '{invoice_price}' is not a valid positive real number."
            if not is_valid("alphanumeric_or_empty_string", vehicle_type)[0]:
                errors["errors_vehicle_type"] = f"'{vehicle_type}' is not a valid vehicle type. It should not have spaces nor special chars. Only letters and numbers."
            if not is_valid("alphanumeric_with_spaces_or_empty_string", model_name)[0]:
                errors["errors_model_name"] = f"'{model_name}' is not a valid model name. It should not have spaces nor special chars. Only letters and numbers."
            if not is_valid("integer", model_year)[0]:
                errors["errors_model_year"] = f"'{model_year}' is not a valid year. It should be an integer."
            else:
                max_year = int(date_added.split("-")[0]) + 2
                if int(model_year) > max_year or int(model_year) < DefaultValues.MIN_MODEL_YEAR:
                    errors["errors_model_year"] = f"'{model_year}' is not a valid year. It should be within range [{DefaultValues.MIN_MODEL_YEAR} - {max_year}]."
            for color in colors:
                if not is_valid("alphanumeric_with_spaces_or_empty_string", color)[0]:
                    errors["errors_colors"] = f"'{color}' is not a valid color. It should not have special chars, only spaces, letters and numbers."
            if not is_valid("positive_decimal_or_empty_string", cargo_capacity)[0]:
                errors["errors_cargo_capacity"] = f"Invalid cargo capacity for Truck. It has to be a number with no letters, spaces nor special chars."
            elif cargo_capacity and float(cargo_capacity) > DefaultValues.MAX_CARGO_CAPACITY:
                errors["errors_cargo_capacity"] = f"Invalid cargo capacity for Truck. It has to be a decimal number less than or equal to {DefaultValues.MAX_CARGO_CAPACITY}."

            if errors:
                return render_template(
                    'newVehicleForm.html',
                    entered_values=entered_data,
                    errors=errors,
                    data=self.data,
                )

            # Validation vs DB data
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(SEQUEL.EXISTS_VIN.format(vin=vin))
                    vin_already_exists = cur.fetchone()['exists']
                    if vin_already_exists:
                        errors['errors_vin'] = "That VIN already exists in our system. Please make sure we don't have that car in inventory or if it was already sold in the past."

                    if errors:
                        return render_template(
                            'newVehicleForm.html',
                            entered_values=entered_data,
                            errors=errors,
                            data=self.data,
                        )
                    
                    # ========================
                    # Insert Data ... finally 
                    # ========================
                    insert_statement_colors = ""
                    for color in colors:
                        insert_statement_colors += f"INSERT INTO Vehicle_Color VALUES ('{vin}', '{color}');"

                    sql_transaction_per_vehicle_type = {
                        "SUV": SEQUEL.INSERT_DATA_SUV,
                        "Convertible": SEQUEL.INSERT_DATA_CONVERTIBLE,
                        "Car": SEQUEL.INSERT_DATA_CAR,
                        "Van": SEQUEL.INSERT_DATA_VAN,
                        "Truck": SEQUEL.INSERT_DATA_TRUCK
                    }

                    transaction = sql_transaction_per_vehicle_type[vehicle_type].format(
                        # All vehicles
                        vin=vin,
                        description=description,
                        invoice_price=invoice_price,
                        type=vehicle_type,
                        model_year=model_year,
                        model_name=model_name,
                        date_added=date_added,
                        clerk_username=clerk_username,
                        manufacturer_name=manufacturer,
                        # SUV
                        number_of_cup_holders=number_of_cup_holders,
                        drivetrain_type=drivetrain_type,
                        # Van
                        has_driver_side_backdoor=has_driver_side_backdoor,
                        # Truck
                        cargo_capacity=cargo_capacity,
                        cargo_cover_type=cargo_cover_type,
                        no_rear_axles=no_rear_axles,
                        # Convertible
                        back_seat_count=back_seat_count,
                        roof_type=roof_type,
                        # Car
                        number_of_doors=number_of_doors,
                        # Colors
                        insert_statement_colors=insert_statement_colors
                    )

                    cur.execute(transaction)
                    # conn.commit()
                flash(f"{description} ({vin}) has been added.", "success")
                return redirect(f'/vehicle/{vin}')

        else:
            return render_template(
                'errorPage.html',
                error_msg="Method not allowed."
            )
