from contextlib import suppress
from datetime import datetime

from flask import request, session, render_template, redirect, flash
import psycopg2

from views.base import Base
from sql_.sequel import SEQUEL
from utils import PSQL, LOG
from utils.utilities import is_valid

class Sale(Base):

    def __init__(self, **kwargs):
        super(Sale, self).__init__(**kwargs)

    def sell(self):
        """
        To sell vehicles
        """

        if request.method == 'POST':

            # Check if it is coming from details page
            target = request.form.get('target')
            vehicle = {
                "vin": request.form.get("vin"),
                "description": request.form.get("description"),
                "invoice_price": request.form.get("invoicePrice"),
                "list_price": request.form.get("listPrice"),
                "colors": request.form.get("colors"),
                "type": request.form.get("vehicleType"),
                "lowest_price": "$ {:.2f}".format(float(request.form.get("invoicePrice").split("$ ")[1]) * 0.95)
            }

            if target == 'find_customer':
                return render_template(
                    'salesOrderForm.html',
                    vehicle=vehicle,
                    customer=dict(),
                    sale=dict(),
                    errors=dict()
                )

            errors = dict()
            customer = dict()

            customer_id = request.form.get("customerID")
            customer = {
                "id": customer_id
            }

            # If customer button is pressed it means it is in the
            customer_button = request.form.get("customerButton")
            sales_button = request.form.get("salesButton")
            if customer_button and customer_button == 'find':
                if not customer_id:
                    errors["customer_id"] = 'This ^^^ field is required.'
                if not is_valid("customer_id", customer_id)[0]:
                    errors["customer_id"] = "Invalid customer ID. Only numbers, letters and dashes allowed."
                if errors:
                    return render_template(
                        'salesOrderForm.html',
                        vehicle=vehicle,
                        customer=customer,
                        sale=dict(),
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
                                'salesOrderForm.html',
                                vehicle=vehicle,
                                customer=customer,
                                sale=dict(),
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
                            'salesOrderForm.html',
                            vehicle=vehicle,
                            customer=customer,
                            sale=dict(),
                            errors=dict()
                        )

            elif customer_button and customer_button == "add":

                vehicle = {
                    "vin": request.form.get("vin"),
                    "description": request.form.get("description"),
                    "invoice_price": request.form.get("invoicePrice"),
                    "list_price": request.form.get("listPrice"),
                    "colors": request.form.get("colors"),
                    "type": request.form.get("vehicleType"),
                    "lowest_price": "$ {:.2f}".format(float(request.form.get("invoicePrice").split("$ ")[1]) * 0.95)
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
                        'salesOrderForm.html',
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
                        'salesOrderForm.html',
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
                        'salesOrderForm.html',
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
                        'salesOrderForm.html',
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
                                'salesOrderForm.html',
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
                        'salesOrderForm.html',
                        customer=customer,
                        errors=errors,
                        vehicle=vehicle,
                        sale=dict()
                    )
            
            elif sales_button and sales_button == "sale":

                sale = dict()

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

                sale_price = request.form.get('salePrice')
                sale_date = request.form.get('saleDate')
                sale['sale_price'] = sale_price
                sale['sale_date'] = sale_date
                
                if not sale_price:
                    errors['sale_price'] = "Sale Price field is required."
                if not sale_date:
                    errors['sale_date'] = "Sale Date field is required."

                if not is_valid("positive_decimal_or_empty_string", sale_price)[0]:
                    errors["sale_price"] = f"Final price '{sale_price}' is not a valid positive real number."
                if not is_valid("date", sale_date)[0]:
                    errors["sale_date"] = f"Sale Date '{sale_date}' is not a valid date. Please insert valid date and follow YYYY-MM-DD format."

                if errors:
                    return render_template(
                        'salesOrderForm.html',
                        vehicle=vehicle,
                        customer=customer,
                        sale=sale,
                        errors=errors
                    )

                if float(sale_price) <= float(vehicle['lowest_price'].split("$ ")[1]) and session['user_info']['role'] not in ['owner']:
                    errors["sale_price"] = f"Final price '{sale_price}' is too low. It has to be at least 95% of Invoice Price ({vehicle['lowest_price']})."

                if float(sale_price) <= 0 and session['user_info']['role'] in ['owner']:
                    errors["sale_price"] = f"Final price '{sale_price}' is not valid. It has to be at least $1 if the owner decides to give it for free."

                # Validating no dates in future
                today = datetime.today()
                
                try:
                    sale_date_date = datetime.strptime(sale_date, '%Y-%m-%d')
                    if sale_date_date > today:
                        errors["sale_date"] = f"Sale Date '{sale_date}' is not valid. It has to be a date in the past, not in future."
                except Exception as ex:
                    LOG.error(f"There was an error: {ex}")
                    errors["sale_date"] = f"Sale Date '{sale_date}' is not valid. Check it please."

                if errors:
                    return render_template(
                        'salesOrderForm.html',
                        vehicle=vehicle,
                        customer=customer,
                        sale=sale,
                        errors=errors
                    )

                # ========================
                # Insert Data ... finally 
                # ========================
                sales_person = session['user_info']['username']
                
                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        cur.execute(SEQUEL.SELL_VEHICLE.format(
                            vin=vehicle['vin'],
                            id=customer['id'],
                            sales_person_username=sales_person,
                            sale_date=sale_date,
                            sold_price="{:.2f}".format(float(sale_price))
                        ))
                
                buyer = None 
                if customer['type'] == 'Individual':
                    buyer = f"""'{customer["firstname"]} {customer["lastname"]}' ({customer["id"]})"""
                if customer['type'] == 'Business':
                    buyer = f"""'{customer["business_name"]}' ({customer['id']})"""
                
                if buyer:
                    msg = f"""Vehicle '{vehicle["description"]}' ({vehicle["vin"]}) has been sold to {buyer}."""
                else:
                    msg = f"""Vehicle '{vehicle["description"]}' ({vehicle["vin"]}) has been sold."""
                flash(msg, 'success')
                return redirect('/')
        
        else:
            return render_template(
                'errorPage.html',
                error_msg="Method not allowed."
            )
