from contextlib import suppress
from datetime import datetime

from flask import request, session, render_template, redirect, flash
import psycopg2

from views.base import Base
from sql_.sequel import SEQUEL
from utils import PSQL, LOG
from utils.utilities import is_valid


# TODO: Dry this controller, way too much repetition
# We needed to deliver and wer running out of time, 
# so we had to apply brute force and copy/paste.
class Repair(Base):

    def __init__(self, **kwargs):
        super(Repair, self).__init__(**kwargs)

    def show(self):
        if request.method == 'GET':
            return render_template(
                'repairsForm.html',
                vehicle=dict()
            )

        if request.method == 'POST':

            vin = request.form.get("vin")

            vehicle = {
                "vin": vin
            }

            errors = dict()

            repair_button = request.form.get("repairButton")
            customer_button = request.form.get("customerButton")
            update_repair_button = request.form.get("updateRepairButton")

            if repair_button and repair_button == 'find':
                if not vin:
                    errors["vin"] = 'VIN field is required.'
                if not is_valid("alphanumeric_or_empty_string", vin)[0]:
                    errors["vin"] = f"'{vin}' is not a valid VIN. It should not have spaces nor special chars. Only letters and numbers."
                if errors:
                    return render_template(
                        'repairsForm.html',
                        vehicle=vehicle,
                        errors=errors
                    )

                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        cur.execute(SEQUEL.SELECT_ALL_VEHICLE_AND_COLORS.format(conditions=f" VIN='{vin}' AND "))
                        existing_vehicle = cur.fetchone()

                        cur.execute(SEQUEL.SELECT_SOLD_VEHICLE_AND_COLORS_IMPROVED.format(vin=vin))
                        sold_vehicle_details = cur.fetchone()

                        cur.execute(SEQUEL.EXISTS_REPAIR_FOR_VIN.format(vin=vin))
                        repair_for_vin_already_exists = cur.fetchone()['exists']
                        
                        if repair_for_vin_already_exists:
                            errors['vin_exists'] = "That VIN is being repaired at the moment. Please wait until that repair is done before starting a new repair."

                        if not sold_vehicle_details:
                            errors['vin'] = "That car is in our system but has not been sold yet. Sell it before repairing it! =) "

                        if not existing_vehicle:
                            errors['vin'] = "That car is not in our system. Try again or add new vehicle if necessary."

                        if errors:
                            return render_template(
                                'repairsForm.html',
                                vehicle=vehicle,
                                errors=errors
                            )

                        vehicle['success'] = True
                        vehicle['description'] = sold_vehicle_details['description']
                        vehicle['type'] = sold_vehicle_details['type']
                        vehicle['model_year'] = sold_vehicle_details['year']
                        vehicle['model_name'] = sold_vehicle_details['mname']
                        vehicle['manufacturer'] = sold_vehicle_details['mfname']
                        vehicle['colors'] = sold_vehicle_details['color']

                        return render_template(
                                'repairsForm.html',
                                vehicle=vehicle,
                                customer=dict(),
                                errors=errors
                            )

            elif customer_button and customer_button == 'find':

                vehicle = {
                    "vin": request.form.get("vin"),
                    "description": request.form.get("description"),
                    "model_year": request.form.get("model_year"),
                    "model_name": request.form.get("model_name"),
                    "manufacturer": request.form.get("manufacturer"),
                    "colors": request.form.get("colors"),
                    "type": request.form.get("vehicleType"),
                    'success': True
                }

                customer_id = request.form.get("customerID")
                customer = {
                    "id": customer_id
                }

                if not customer_id:
                    errors["customer_id"] = 'This ^^^ field is required.'
                if not is_valid("customer_id", customer_id)[0]:
                    errors["customer_id"] = "Invalid customer ID. Only numbers, letters and dashes allowed."
                if errors:
                    return render_template(
                        'repairsForm.html',
                        vehicle=vehicle,
                        customer=customer,
                        errors=errors
                    )

                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        cur.execute(SEQUEL.SELECT_INDIVIDUAL_CUSTOMER.format(customerID=customer_id))
                        individual_customer = cur.fetchone()

                        cur.execute(SEQUEL.SELECT_BUSINESS_CUSTOMER.format(customerID=customer_id))
                        business_customer = cur.fetchone()

                        if not individual_customer and not business_customer:
                            errors['customer_id'] = "That customer doesn't exist. Try again or add new customer if necessary."

                        if errors:
                            return render_template(
                                'repairsForm.html',
                                vehicle=vehicle,
                                customer=customer,
                                errors=errors
                            )

                        if individual_customer:
                            customer['type'] = 'Individual'
                            customer['address'] = individual_customer['address']
                            customer['phone_number'] = individual_customer['phonenumber']
                            customer['email_address'] = individual_customer['emailaddress']
                            customer['firstname'] = individual_customer['firstname']
                            customer['lastname'] = individual_customer['lastname']
                            customer['success'] = True
                        elif business_customer:
                            customer['type'] = 'Business'
                            customer['address'] = business_customer['address']
                            customer['phone_number'] = business_customer['phonenumber']
                            customer['email_address'] = business_customer['emailaddress']
                            customer['business_name'] = business_customer['bname']
                            customer['person_name'] = business_customer['pcname']
                            customer['person_title'] = business_customer['title']
                            customer['success'] = True

                        return render_template(
                            'repairsForm.html',
                            vehicle=vehicle,
                            customer=customer,
                            errors=dict(),
                            repair=dict()
                        )


            elif customer_button and customer_button == "add":

                vehicle = {
                    "vin": request.form.get("vin"),
                    "description": request.form.get("description"),
                    "model_year": request.form.get("model_year"),
                    "model_name": request.form.get("model_name"),
                    "manufacturer": request.form.get("manufacturer"),
                    "colors": request.form.get("colors"),
                    "type": request.form.get("vehicleType"),
                    'success': True
                }

                # Get common data submitted user
                account_type = request.form.get("accountType")
                customer_id = request.form.get("customerID")

                # Get info individual
                firstname = request.form.get('add_firstname')
                lastname = request.form.get('add_lastname')
                individual_phone_number = request.form.get('add_phoneNumber_individual')
                individual_address = request.form.get('add_address_individual')
                individual_email = request.form.get('add_email_individual', '')

                # Get info business
                business_primary_contact_name = request.form.get('add_primaryContactName')
                business_primary_contact_title = request.form.get('add_primaryContactTitle')
                business_name = request.form.get('add_businessName')
                business_phone_number = request.form.get('add_phoneNumber_business')
                business_email = request.form.get('add_email_business', '')
                business_address = request.form.get('add_address_business')

                # Capture all entered data to display back if necessary (if errors)
                customer = {
                    'id': customer_id,
                    'add_firstname': firstname,
                    'add_lastname': lastname,
                    'add_phone_number_individual': individual_phone_number,
                    'add_address_individual': individual_address,
                    'add_email_individual': individual_email,
                    'add_business_name': business_name,
                    'add_primary_contact_name': business_primary_contact_name,
                    'add_primary_contact_title': business_primary_contact_title,
                    'add_address_business': business_address,
                    'add_phone_number_business': business_phone_number,
                    'add_email_business': business_email,
                }

                # Validate input
                # Validate against no values submitted
                errors = dict()
                errors["add_customer"] = ""
                if not customer_id:
                    errors["add_customer"] += 'CustomerID field is required. '
                if not account_type:
                    errors["add_customer"] += 'Account Type selection is required. '

                if errors.get("add_customer"):
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle
                    )

                if account_type == 'Business':
                    if not business_primary_contact_name:
                        errors["add_customer"] += 'Primary Contact Name field for Business is required. '
                    if not business_primary_contact_title:
                        errors["add_customer"] += 'Primary Contact Title field for Business is required. '
                    if not business_name:
                        errors["add_customer"] += 'Business Name field for Business is required. '
                    if not business_phone_number:
                        errors["add_customer"] += 'Phone Number field for Business is required. '
                    # if not business_email:
                    #     errors["add_customer"] += 'Email field for Business is required. '
                    if not business_address:
                        errors["add_customer"] += 'Address field for Business is required. '

                elif account_type == 'Individual':
                    if not firstname:
                        errors["add_customer"] += 'Firstname field for Individual is required. '
                    if not lastname:
                        errors["add_customer"] += 'Lastname field for Individual is required. '
                    if not individual_phone_number:
                        errors["add_customer"] += 'Phone Number field for Individual is required. '
                    if not individual_address:
                        errors["add_customer"] += 'Address field for Individual is required. '
                    # if not individual_email:
                    #     errors["add_customer"] += 'Email field for Individual is required. '
                
                if errors.get("add_customer"):
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle
                    )

                if customer_id and len(customer_id) > 30:
                    errors["add_customer"] += 'Customer ID field is too long. It has to be 30 chars max. '

                if account_type == 'Business':
                    if len(business_primary_contact_name) > 100:
                        errors["add_customer"] += 'Primary Contact Name field for Business is too long (max 100 chars). '
                    if len(business_primary_contact_title) > 50:
                        errors["add_customer"] += 'Primary Contact Title field for Business is too long (max 50 chars). '
                    if len(business_name) > 100:
                        errors["add_customer"] += 'Business Name field for Business is too long (max 100 chars). '
                    if len(business_phone_number) > 20:
                        errors["add_customer"] += 'Phone Number field for Business is too long (max 15 chars). '
                    if len(business_email) > 50:
                        errors["add_customer"] += 'Email field for Business is too long (max 50 chars). '
                    if len(business_address) > 200:
                        errors["add_customer"] += 'Address field for Business is too long (max 200 chars). '

                elif account_type == 'Individual':
                    if len(firstname) > 30:
                        errors["add_customer"] += 'Firstname field for Individual is too long (max 30 chars). '
                    if len(lastname) > 30:
                        errors["add_customer"] += 'Lastname field for Individual is too long (max 30 chars). '
                    if len(individual_phone_number) > 20:
                        errors["add_customer"] += 'Phone Number field for Individual is too long (max 15 chars). '
                    if len(individual_email) > 50:
                        errors["add_customer"] += 'Email field for Individual is too long (max 50 chars). '
                    if len(individual_address) > 200:
                        errors["add_customer"] += 'Address field for Individual is too long (max 200 chars). '

                if errors.get("add_customer"):
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle
                    )

                if not is_valid("customer_id", customer_id)[0]:
                    errors["add_customer"] += 'Customer ID is invalid. '

                # Validate specifics and repel SQL Injection
                if account_type == 'Business':
                    if not is_valid("composed_name", business_primary_contact_name)[0]:
                        errors["add_customer"] += 'Primary Contact Name is not valid, please use only letters and spaces. '
                    if not is_valid("business_name", business_primary_contact_title)[0]:
                        errors["add_customer"] += 'Primary Contact Title is not valid, please use only letters, numbers, spaces and special chars [,.-#]. '
                    if not is_valid("business_name", business_name)[0]:
                        errors["add_customer"] += 'Business Name is not valid, please use only letters, numbers, spaces and special chars [,.-#]. '
                    if not is_valid("phone_number", business_phone_number)[0]:
                        errors["add_customer"] += 'Phone Number is not valid. '
                    if not is_valid("email", business_email)[0]:
                        errors["add_customer"] += 'Email is not valid. '
                    if not is_valid("address", business_address)[0]:
                        errors["add_customer"] += 'Address is invalid. '

                elif account_type == 'Individual':
                    if not is_valid("word", firstname):
                        errors["add_customer"] += 'Firstname is invalid, please use only letters. '
                    if not is_valid("word", lastname):
                        errors["add_customer"] += 'Lastname is invalid, please use only letters. '
                    if not is_valid("phone_number", individual_phone_number)[0]:
                        errors["add_customer"] += 'Phone Number is not valid. '
                    if not is_valid("email", individual_email)[0]:
                        errors["add_customer"] += 'Email is not valid. '
                    if not is_valid("address", individual_address)[0]:
                        errors["add_customer"] += 'Address is invalid. '

                if errors.get("add_customer"):
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle
                    )

                # Validation vs DB data
                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        cur.execute(SEQUEL.EXISTS_CUSTOMER_ID.format(customer_id=customer_id))
                        customer_already_exists = cur.fetchone()['exists']
                        if customer_already_exists:
                            errors['add_customer'] = "That customer already exists in our system. Use `Find` option instead. "

                        if errors.get("add_customer"):
                            return render_template(
                                'repairsForm.html',
                                customer=customer,
                                errors=errors,
                                vehicle=vehicle
                            )
                        
                        if account_type == "Individual":
                            transaction = SEQUEL.INSERT_DATA_INDIVIDUAL.format(
                                # All customers
                                id=customer_id,
                                address=individual_address,
                                phone_number=individual_phone_number,
                                email_address=individual_email,
                                # Individual
                                driver_license_number=customer_id,
                                firstname=firstname,
                                lastname=lastname
                            )

                            customer['type'] = account_type
                            customer['address'] = individual_address
                            customer['phone_number'] = individual_phone_number
                            customer['email_address'] = individual_email
                            customer['firstname'] = firstname
                            customer['lastname'] = lastname
                            customer['success'] = True

                            flash_msg = f"Customer {firstname} {lastname} ({customer_id}) has been added."

                        elif account_type == "Business":
                            transaction = SEQUEL.INSERT_DATA_BUSINESS.format(
                                # All customers
                                id=customer_id,
                                address=business_address,
                                phone_number=business_phone_number,
                                email_address=business_email,
                                # Business
                                tin=customer_id,
                                business_name=business_name,
                                primary_contact_name=business_primary_contact_name,
                                primary_contact_title=business_primary_contact_title
                            )

                            customer['type'] = account_type
                            customer['address'] = business_address
                            customer['phone_number'] = business_phone_number
                            customer['email_address'] = business_address
                            customer['business_name'] = business_name
                            customer['person_name'] = business_primary_contact_name
                            customer['person_title'] = business_primary_contact_title
                            customer['success'] = True

                            flash_msg = f"Customer {business_name} ({customer_id}) has been added."

                        cur.execute(transaction)

                    flash(flash_msg, "success")
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle,
                        repair=dict()
                    )

            elif repair_button and repair_button == "create":

                vehicle = {
                    "vin": request.form.get("vin"),
                    "description": request.form.get("description"),
                    "model_year": request.form.get("model_year"),
                    "model_name": request.form.get("model_name"),
                    "manufacturer": request.form.get("manufacturer"),
                    "colors": request.form.get("colors"),
                    "type": request.form.get("vehicleType"),
                    'success': True
                }

                customer = {
                    "id": request.form.get("customerID"),
                    "type": request.form.get("successCustomerType"),
                    'address': request.form.get("successCustomerAddress"),
                    'phone_number': request.form.get("successCustomerPhoneNumber"),
                    'email_address': request.form.get("successCustomerEmailAddress", ''),
                    'firstname': request.form.get("successCustomerFirstname"),
                    'lastname': request.form.get("successCustomerLastname"),
                    'business_name': request.form.get("successCustomerBusinessName"),
                    'person_name': request.form.get("successCustomerPersonName"),
                    'person_title': request.form.get("successCustomerPersonTitle"),
                    'success': True
                }

                repair_description = request.form.get('add_repairDescription')
                odomoter_reading = request.form.get('add_repairOdometer')

                repair = {
                    'description': repair_description,
                    'odometer': odomoter_reading
                }

                # Validate input
                # Validate against no values submitted
                errors = dict()
                if not repair_description:
                    errors["add_repairDescription"] = 'Repair Description is required.'
                elif len(repair_description) > 500:
                    errors["add_repairDescription"] = 'Repair Description field is too long (max 500 chars). '
                if not odomoter_reading:
                    errors["add_repairOdometer"] = 'Odometer Reading is required.'

                if errors:
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle,
                        repair=repair
                    )

                if not is_valid("positive_decimal_or_empty_string", odomoter_reading)[0]:
                    errors["add_repairOdometer"] = 'Odometer Reading is invalid. Only positive numbers, please.'

                if not is_valid("address", repair_description)[0]:
                    errors["add_repairDescription"] = 'Repair Description is invalid. Try to minimize use of special chars.'

                if errors:
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle,
                        repair=repair
                    )

                # Add data
                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        cur.execute(SEQUEL.SELECT_REPAIR.format(
                            vin=vehicle.get("vin"),
                            customer_id=customer.get("id"),
                            start_date=datetime.today().strftime('%Y-%m-%d')
                        ))
                        exists_repair = cur.fetchone()
                        if exists_repair:
                            errors["add_repairOdometer"] = 'Not possible to create new repair. There was already a repair for today with that customer and vin. Try tomorrow.'
                        else:
                            transaction = SEQUEL.INSERT_INTO_REPAIR.format(
                                vin=vehicle['vin'],
                                customer_id=customer['id'],
                                start_date=datetime.today().strftime('%Y-%m-%d'),
                                service_writer_username=session['user_info']['username'],
                                repair_description=repair_description,
                                odometer_reading=odomoter_reading
                            )
                            try:
                                cur.execute(transaction)
                            except psycopg2.errors.UniqueViolation:
                                errors['repairs'] = "There is already a repair for this VIN going on."
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair
                                )
                            repair['labor_charges'] = "0.00"
                            repair['success'] = True
                            flash("Repair added", "success")
                    
                    return render_template(
                        'repairsForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle,
                        repair=repair,
                        new_part=dict()
                    )

            elif update_repair_button and update_repair_button == "go_to_update":

                vin = request.form.get("vin")

                vehicle = {
                    "vin": vin
                }

                errors = dict()

                if not vin:
                    errors["vin"] = 'VIN field is required.'
                if not is_valid("alphanumeric_or_empty_string", vin)[0]:
                    errors["vin"] = f"'{vin}' is not a valid VIN. It should not have spaces nor special chars. Only letters and numbers."
                if errors:
                    return render_template(
                        'repairsForm.html',
                        vehicle=vehicle,
                        errors=errors
                    )

                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        cur.execute(SEQUEL.SELECT_ALL_VEHICLE_AND_COLORS.format(conditions=f" VIN='{vin}' AND "))
                        existing_vehicle = cur.fetchone()

                        cur.execute(SEQUEL.SELECT_SOLD_VEHICLE_AND_COLORS_IMPROVED.format(vin=vin))
                        sold_vehicle_details = cur.fetchone()

                        cur.execute(SEQUEL.EXISTS_REPAIR_FOR_VIN.format(vin=vin))
                        repair_for_vin_already_exists = cur.fetchone()['exists']
                        
                        if not repair_for_vin_already_exists:
                            errors['vin_exists'] = "That VIN is not being repaired at the moment. Create a repair before trying to update one."

                        if not sold_vehicle_details:
                            errors['vin'] = "That car is in our system but has not been sold yet. Sell it before repairing it! =) "

                        if not existing_vehicle:
                            errors['vin'] = "That car is not in our system. Try again or add new vehicle if necessary."

                        if errors:
                            return render_template(
                                'repairsForm.html',
                                vehicle=vehicle,
                                errors=errors
                            )

                        cur.execute(SEQUEL.SELECT_ALL_INFO_FOR_REPAIR.format(vin=vin))
                        repair_info = cur.fetchone()

                        cur.execute(SEQUEL.SELECT_ONLY_VEHICLE_AND_COLOR_IMPROVED.format(vin=vin))
                        colors = cur.fetchone()['colors']

                        cur.execute(SEQUEL.IS_CUSTOMER_INDIVIDUAL.format(id_=repair_info.get("id")))
                        is_customer_individual = cur.fetchone()['exists']

                        cur.execute(SEQUEL.IS_CUSTOMER_BUSINESS.format(id_=repair_info.get("id")))
                        is_customer_business = cur.fetchone()['exists']

                        cur.execute(SEQUEL.SELECT_PARTS.format(
                            vin=repair_info.get("vin"),
                            customer_id=repair_info.get("id"),
                            start_date=repair_info.get("startdate")
                        ))
                        parts = cur.fetchall()

                        # TODO: Handle unknown customer type. Here we assume we will find user in either Business or Individual.
                        customer_type = 'Individual' if is_customer_individual else 'Business' if is_customer_business else 'Unknown'

                        vehicle = {
                            "vin": repair_info.get("vin"),
                            "description": repair_info.get("description"),
                            "model_year": repair_info.get("year"),
                            "model_name": repair_info.get("mname"),
                            "manufacturer": repair_info.get("mfname"),
                            "colors": colors,
                            "type": repair_info.get("type"),
                            'success': True
                        }

                        customer = {
                            "id": repair_info.get("id"),
                            "type": customer_type,
                            'address': repair_info.get("address"),
                            'phone_number': repair_info.get("phonenumber"),
                            'email_address': repair_info.get("emailaddress"),
                            'firstname': repair_info.get("firstname"),
                            'lastname': repair_info.get("lastname"),
                            'business_name': repair_info.get("bname"),
                            'person_name': repair_info.get("pcname"),
                            'person_title': repair_info.get("title"),
                            'success': True
                        }

                        repair = {
                            'description': repair_info.get("rdescription"),
                            'odometer': repair_info.get("odometerreading"),
                            'labor_charges': "{:.2f}".format(float(repair_info.get("laborcharges") or 0)),
                            'success': True
                        }

                        return render_template(
                            'repairsForm.html',
                            customer=customer,
                            errors=errors,
                            vehicle=vehicle,
                            repair=repair,
                            parts=parts,
                            new_part=dict()
                        )

            elif repair_button and repair_button in ["update_labor", "complete", "add_part", "delete_part"]:

                vin = request.form.get("vin")

                vehicle = {
                    "vin": vin
                }

                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                        cur.execute(SEQUEL.SELECT_ALL_INFO_FOR_REPAIR.format(vin=vin))
                        repair_info = cur.fetchone()

                        cur.execute(SEQUEL.SELECT_ONLY_VEHICLE_AND_COLOR_IMPROVED.format(vin=vin))
                        colors = cur.fetchone()['colors']

                        cur.execute(SEQUEL.IS_CUSTOMER_INDIVIDUAL.format(id_=repair_info.get("id")))
                        is_customer_individual = cur.fetchone()['exists']

                        cur.execute(SEQUEL.IS_CUSTOMER_BUSINESS.format(id_=repair_info.get("id")))
                        is_customer_business = cur.fetchone()['exists']

                        # TODO: Handle unknown customer type. Here we assume we will find user in either Business or Individual.
                        customer_type = 'Individual' if is_customer_individual else 'Business' if is_customer_business else 'Unknown'

                        vehicle = {
                            "vin": repair_info.get("vin"),
                            "description": repair_info.get("description"),
                            "model_year": repair_info.get("year"),
                            "model_name": repair_info.get("mname"),
                            "manufacturer": repair_info.get("mfname"),
                            "colors": colors,
                            "type": repair_info.get("type"),
                            'success': True
                        }

                        customer = {
                            "id": repair_info.get("id"),
                            "type": customer_type,
                            'address': repair_info.get("address"),
                            'phone_number': repair_info.get("phonenumber"),
                            'email_address': repair_info.get("emailaddress"),
                            'firstname': repair_info.get("firstname"),
                            'lastname': repair_info.get("lastname"),
                            'business_name': repair_info.get("bname"),
                            'person_name': repair_info.get("pcname"),
                            'person_title': repair_info.get("title"),
                            'success': True
                        }

                        repair = {
                            'description': repair_info.get("rdescription"),
                            'odometer': repair_info.get("odometerreading"),
                            'start_date': repair_info.get("startdate"),
                            'labor_charges': "{:.2f}".format(float(repair_info.get("laborcharges") or 0)),
                            'success': True
                        }

                        cur.execute(SEQUEL.SELECT_PARTS.format(
                            vin=repair_info.get("vin"),
                            customer_id=repair_info.get("id"),
                            start_date=repair_info.get("startdate")
                        ))
                        parts = cur.fetchall()

                        if repair_button == "update_labor":
                            labor_charges = request.form.get('add_laborCharges')
                            repair['add_labor_charges'] = labor_charges

                            errors = dict()
                            if not is_valid("positive_decimal_or_empty_string", labor_charges)[0]:
                                errors['add_repair_labor_changes'] = "New labor charges amount entered is not a valid positive real number."

                            if not labor_charges or errors:
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair,
                                    parts=parts,
                                    new_part=dict()
                                )

                            cur.execute(SEQUEL.SELECT_REPAIR.format(
                                vin=repair_info.get("vin"),
                                customer_id=repair_info.get("id"),
                                start_date=repair_info.get("startdate")
                            ))

                            existing_labor_charges = cur.fetchone()['laborcharges']
                            if existing_labor_charges > float(labor_charges):
                                errors['add_repair_labor_changes'] = "New labor charges amount entered has to be higher than existing amount."
                            else:
                                cur.execute(SEQUEL.UPDATE_REPAIR_LABOR_CHARGES.format(
                                    vin=repair_info.get("vin"),
                                    customer_id=repair_info.get("id"),
                                    start_date=repair_info.get("startdate"),
                                    new_labor_charges=labor_charges
                                ))
                                repair['labor_charges'] = "{:.2f}".format(float(labor_charges) or 0)
                            return render_template(
                                'repairsForm.html',
                                customer=customer,
                                errors=errors,
                                vehicle=vehicle,
                                repair=repair,
                                parts=parts,
                                new_part=dict()
                            )
                        
                        elif repair_button == "complete":
                            cur.execute(SEQUEL.COMPLETE_REPAIR.format(
                                vin=repair_info.get("vin"),
                                customer_id=repair_info.get("id"),
                                start_date=repair_info.get("startdate"),
                                completion_date=datetime.today().strftime('%Y-%m-%d')
                            ))

                            flash(f'''Repair '{repair_info.get("vin")}:{repair_info.get("id")}:{repair_info.get("startdate")}' was completed.''', 'success')
                            return redirect('/')

                        elif repair_button == 'add_part':

                            # Get part data submitted user
                            new_part_part_number = request.form.get('new_part_part_number')
                            new_part_vendor_name = request.form.get('new_part_vendor_name')
                            new_part_quantity = request.form.get('new_part_quantity')
                            new_part_unit_price = request.form.get('new_part_unit_price')

                            new_part = {
                                'part_number': new_part_part_number,
                                'vendor_name': new_part_vendor_name,
                                'quantity': new_part_quantity,
                                'unit_price': new_part_unit_price
                            }

                            errors = dict()
                            # Validate input
                            if not new_part_part_number:
                                errors["new_part_part_number"] = 'Part Number is required.'
                            if not new_part_vendor_name:
                                errors["new_part_vendor_name"] = 'Vendor Name is required.'
                            if not new_part_quantity:
                                errors["new_part_quantity"] = 'Quantity is required.'
                            if not new_part_unit_price:
                                errors["new_part_unit_price"] = 'Unit Price is required.'

                            if errors:
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair,
                                    parts=parts,
                                    new_part=new_part
                                )

                            if len(new_part_part_number) > 50:
                                errors["new_part_part_number"] = 'Part Number field is too long. It has to be 50 chars max.'
                            if len(new_part_vendor_name) > 50:
                                errors["new_part_vendor_name"] = 'Vendor Name field is too long (max 50 chars).'
                            
                            if errors:
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair,
                                    parts=parts,
                                    new_part=new_part
                                )

                            if not is_valid("part_number", new_part_part_number)[0]:
                                errors["new_part_part_number"] = 'Part Number is invalid. Only alphanumeric and [._-] allowed.'
                            if not is_valid("address", new_part_vendor_name)[0]:
                                errors["new_part_vendor_name"] = 'Vendor name is invalid. Only alphanumeric and [-,.# ] allowed.'
                            if not is_valid("integer", new_part_quantity)[0]:
                                errors["new_part_quantity"] = 'Quantity is invalid. Only integers allowed.'
                            elif int(new_part_quantity) > 32766:
                                errors["new_part_quantity"] = 'Quantity is too big. If higher than `32766` please add in another entry.'
                            if not is_valid("positive_decimal_or_empty_string", new_part_unit_price)[0]:
                                errors['new_part_unit_price'] = "Unit Price is not a valid positive real number."

                            if errors:
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair,
                                    parts=parts,
                                    new_part=new_part
                                )

                            cur.execute(SEQUEL.EXISTS_PART.format(
                                vin=vehicle['vin'],
                                customer_id=customer['id'],
                                start_date=repair['start_date'],
                                part_number=new_part_part_number,
                                vendor_name=new_part_vendor_name,
                                price=new_part_unit_price
                            ))
                            part_already_exists = cur.fetchone()['exists']
                            if part_already_exists:
                                errors['new_part_overall'] = "That part number already exists for this repair, with same"
                                errors['new_part_overall'] += " vendor and price. If you want to update then first DELETE and then ADD new."
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair,
                                    parts=parts,
                                    new_part=new_part
                                )
                            else:
                                cur.execute(SEQUEL.INSERT_INTO_PARTS.format(
                                    vin=vehicle['vin'],
                                    customer_id=customer['id'],
                                    start_date=repair['start_date'],
                                    part_number=new_part_part_number,
                                    vendor_name=new_part_vendor_name,
                                    quantity=new_part_quantity,
                                    price=new_part_unit_price
                                ))

                                cur.execute(SEQUEL.SELECT_PARTS.format(
                                    vin=repair_info.get("vin"),
                                    customer_id=repair_info.get("id"),
                                    start_date=repair_info.get("startdate")
                                ))
                                parts = cur.fetchall()

                                flash("Part added succesfully", "success")
                                return render_template(
                                    'repairsForm.html',
                                    customer=customer,
                                    errors=errors,
                                    vehicle=vehicle,
                                    repair=repair,
                                    parts=parts,
                                    new_part=dict()
                                )

                        elif repair_button == 'delete_part':

                            part_number = request.form.get('displayed_part__part_number')
                            vendor_name = request.form.get('displayed_part__vendor_name')
                            unit_price = request.form.get('displayed_part__unit_price')

                            cur.execute(SEQUEL.DELETE_PART.format(
                                vin=vehicle['vin'],
                                customer_id=customer['id'],
                                start_date=repair['start_date'],
                                part_number=part_number,
                                vendor_name=vendor_name,
                                price=unit_price
                            ))

                            cur.execute(SEQUEL.SELECT_PARTS.format(
                                vin=repair_info.get("vin"),
                                customer_id=repair_info.get("id"),
                                start_date=repair_info.get("startdate")
                            ))
                            parts = cur.fetchall()

                            flash("Part removed succesfully", "warning")
                            return render_template(
                                'repairsForm.html',
                                customer=customer,
                                errors=errors,
                                vehicle=vehicle,
                                repair=repair,
                                parts=parts,
                                new_part=dict()
                            )

        else:
            return render_template(
                'errorPage.html',
                error_msg="Method not allowed."
            )
