from flask import request, render_template, flash, session, redirect, url_for
import psycopg2
from contextlib import suppress
from collections import OrderedDict

from views.base import Base 
from cmd_.default_values import DefaultValues
from sql_.sequel import SEQUEL
from utils import PSQL, LOG
from utils.utilities import is_valid

class Search(Base):
    """
    Will search only unsold vehicles
    """

    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)

    def search(self):
        with PSQL.get_DB_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                self.count_unsold_cars = self.get_unsold_cars_count(cur)
                self.vehicle_type_and_count = self.get_vehicle_type_and_count_for_unsold_cars(cur)
                self.all_manufacturers = self.get_all_manufacturers(cur)
                self.manufacturers_and_count = self.get_manufacturers_and_count_for_unsold_cars(cur)
                self.model_year_and_count = self.get_models_years_and_count(cur)
                self.colors_and_count = self.get_colors_and_count_for_unsold_cars(cur)

        if request.method == 'GET':
            return render_template(
                'searchPage.html', 
                count_unsold_cars=self.count_unsold_cars, 
                vehicle_types_and_counts=self.merge_vehicle_types_and_counts(
                    self.vehicle_type_and_count, DefaultValues.AVAILABLE_VEHICLE_TYPES),
                manufacturers_and_counts=self.merge_items_and_counts(
                    self.manufacturers_and_count, self.all_manufacturers, 'mfname'),
                models_years_and_counts=self.generate_and_merge_range_model_year_counts(
                    self.model_year_and_count),
                colors_and_counts=self.merge_colors_and_counts(
                    self.colors_and_count, DefaultValues.AVAILABLE_COLORS),
                entered_values=dict(),
                errors=dict()
            )
        elif request.method == 'POST':

            errors = dict()
            entered_values = dict()

            vin_ = request.form.get("vinTextBox")
            entered_values["vin"] = vin_

            sold_unsold_all_option = request.form.get('sold_unsold_all_option_radio')
            SOLD_UNSOLD_ALL_QUERIES = {
                "unsold": SEQUEL.SELECT_UNSOLD_VEHICLE_AND_COLORS,
                "sold": SEQUEL.SELECT_SOLD_VEHICLE_AND_COLORS,
                "all": SEQUEL.SELECT_ALL_VEHICLE_AND_COLORS
            }
            query_vehicles = SOLD_UNSOLD_ALL_QUERIES.get(sold_unsold_all_option, SEQUEL.SELECT_UNSOLD_VEHICLE_AND_COLORS)

            color = None
            with suppress(Exception):
                color = request.form.get("colorSelect1").split(" (")[0]

            manufacturer = None
            with suppress(Exception):
                manufacturer = request.form.get("manufacturerSelect1").split(" (")[0]

            model_year = None
            with suppress(Exception):
                model_year = request.form.get("modelYearSelect1").split(" (")[0]

            vehicle_type = None
            with suppress(Exception):
                vehicle_type = request.form.get("vehicleTypeSelect1").split(" (")[0]

            list_price_option = request.form.get("listPriceOption")

            keyword_ = request.form.get("keywordTextBox") or ''
            if not is_valid("alphanumeric_with_spaces_or_empty_string", keyword_)[0]:
                errors["keyword_error"] = "Keyword is not valid. Only numbers, letters, spaces or no text allowed. Please try again."
            entered_values["keyword_"] = keyword_

            list_price = None
            with suppress(Exception):
                list_price = request.form.get("listPriceText").strip()
                if not is_valid("positive_decimal_or_empty_string", list_price)[0]:
                    errors["list_price_error"] = "List price is not valid positive decimal nor empty. Please try again."
            entered_values["list_price"] = list_price
            
            if errors:
                LOG.error(f"There were errors: {errors}")
                return render_template(
                    'searchPage.html', 
                    count_unsold_cars=self.count_unsold_cars, 
                    vehicle_types_and_counts=self.merge_vehicle_types_and_counts(
                        self.vehicle_type_and_count, DefaultValues.AVAILABLE_VEHICLE_TYPES),
                    manufacturers_and_counts=self.merge_items_and_counts(
                        self.manufacturers_and_count, self.all_manufacturers, 'mfname'),
                    models_years_and_counts=self.generate_and_merge_range_model_year_counts(
                        self.model_year_and_count),
                    colors_and_counts=self.merge_colors_and_counts(
                        self.colors_and_count, DefaultValues.AVAILABLE_COLORS),
                    entered_values=entered_values,
                    errors=errors
                )
            else:
                results = dict()
                with PSQL.get_DB_connection() as conn:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                        
                        # Get all cars that are within the price range
                        price_constraint_condition = ""
                        vehicles_within_price_range = list()
                        if list_price_option == 'lte' and list_price:
                            price_constraint_condition = f"InvoicePrice *1.25 <= {list_price} AND "
                        elif list_price_option == 'gte' and list_price:
                            price_constraint_condition = f"InvoicePrice *1.25 >= {list_price} AND "

                        if price_constraint_condition:
                            query = query_vehicles.format(
                                conditions=price_constraint_condition
                            )
                            cur.execute(query)
                            for item in cur.fetchall():
                                if item['vin'] not in vehicles_within_price_range:
                                    vehicles_within_price_range.append(item['vin'])

                        # Filters vehicles by conditions
                        # and add only those that comply with price range
                        conditions = ""
                        if vin_:
                            conditions += f"vin = '{vin_}' AND "
                        if color:
                            conditions += f"Color = '{color}' AND "
                        if manufacturer:
                            conditions += f"MFName = '{manufacturer}' AND "
                        if model_year:
                            conditions += f"Year = '{model_year}' AND "
                        if vehicle_type:
                            conditions += f"Type = '{vehicle_type}' AND "
                        if list_price_option == 'lte' and list_price:
                            conditions = conditions[:-4] + "AND " if conditions else ""
                            conditions += f"InvoicePrice *1.25 <= {list_price} AND "
                        elif list_price_option == 'gte' and list_price:
                            conditions = conditions[:-4] + "AND " if conditions else ""
                            conditions += f"InvoicePrice *1.25 >= {list_price} AND "

                        if conditions:
                            query1 = query_vehicles.format(
                                conditions=conditions,
                            )
                            cur.execute(query1)
                            for item in cur.fetchall():
                                if list_price:
                                    if item['vin'] in vehicles_within_price_range:
                                        if item['vin'] in results:
                                            if item['color'] not in results[item['vin']]['colors']:
                                                results[item['vin']]['colors'] += f",{item['color']}"
                                        else:
                                            results[item['vin']] = {
                                                "vehicle_type": item['type'],
                                                "model_year": item['year'],
                                                "manufacturer": item['mfname'],
                                                "model_name": item['mname'],
                                                "colors": item['color'],
                                                "matched_keyword": "",
                                                "list_price": "$ {:.2f}".format(float(item['listprice']))
                                            }
                                else:
                                    if item['vin'] in results:
                                        if item['color'] not in results[item['vin']]['colors']:
                                            results[item['vin']]['colors'] += f",{item['color']}"
                                    else:
                                        results[item['vin']] = {
                                            "vehicle_type": item['type'],
                                            "model_year": item['year'],
                                            "manufacturer": item['mfname'],
                                            "model_name": item['mname'],
                                            "colors": item['color'],
                                            "matched_keyword": "",
                                            "list_price": "$ {:.2f}".format(float(item['listprice']))
                                        }

                        # Search cars and add only those that comply with price range
                        if keyword_:
                            conditions_keyword = f"""MFName LIKE '%{keyword_}%'
                                                    OR Year::VARCHAR LIKE '%{keyword_}%' 
                                                    OR MName LIKE '%{keyword_}%' 
                                                    OR Description LIKE '%{keyword_}%' AND """

                            query2 = query_vehicles.format(
                                conditions=conditions_keyword
                            )
                            cur.execute(query2)
                            for item in cur.fetchall():
                                if list_price:
                                    if item['vin'] in vehicles_within_price_range:
                                        if item['vin'] in results:
                                            if item['color'] not in results[item['vin']]['colors']:
                                                results[item['vin']]['colors'] += f",{item['color']}"
                                            results[item['vin']]['matched_keyword'] = 'X'
                                        else: 
                                            results[item['vin']] = {
                                                "vehicle_type": item['type'],
                                                "model_year": item['year'],
                                                "manufacturer": item['mfname'],
                                                "model_name": item['mname'],
                                                "colors": item['color'],
                                                "matched_keyword": "X",
                                                "list_price": "$ {:.2f}".format(float(item['listprice']))
                                            }
                                else:
                                    if item['vin'] in results:
                                        if item['color'] not in results[item['vin']]['colors']:
                                            results[item['vin']]['colors'] += f",{item['color']}"
                                        results[item['vin']]['matched_keyword'] = 'X'
                                    else: 
                                        results[item['vin']] = {
                                            "vehicle_type": item['type'],
                                            "model_year": item['year'],
                                            "manufacturer": item['mfname'],
                                            "model_name": item['mname'],
                                            "colors": item['color'],
                                            "matched_keyword": "X",
                                            "list_price": "$ {:.2f}".format(float(item['listprice']))
                                        }

                        # Get and merge all colors
                        if results:
                            in_expression = tuple(results.keys()) if len(list(results.keys())) > 1 else f"('{list(results.keys())[0]}')"
                            conditions = f"VIN IN {in_expression} AND "
                            query_colors = SEQUEL.SELECT_ONLY_VEHICLE_AND_COLOR.format(
                                conditions=conditions,
                            )
                            cur.execute(query_colors)
                            for item in cur.fetchall():
                                if item['color'] not in results[item['vin']]['colors']:
                                    results[item['vin']]['colors'] += f",{item['color']}"

                if not results:
                    errors["results_error"] = "Sorry, it looks like we don’t have that in stock!"
                else:
                    results = OrderedDict(sorted(results.items()))

                return render_template(
                    'searchPage.html', 
                    count_unsold_cars=self.count_unsold_cars, 
                    vehicle_types_and_counts=self.merge_vehicle_types_and_counts(
                        self.vehicle_type_and_count, DefaultValues.AVAILABLE_VEHICLE_TYPES),
                    manufacturers_and_counts=self.merge_items_and_counts(
                        self.manufacturers_and_count, self.all_manufacturers, 'mfname'),
                    models_years_and_counts=self.generate_and_merge_range_model_year_counts(
                        self.model_year_and_count),
                    colors_and_counts=self.merge_colors_and_counts(
                        self.colors_and_count, DefaultValues.AVAILABLE_COLORS),
                    entered_values=entered_values,
                    errors=errors,
                    results=results
                )

        else:
            return render_template(
                'errorPage.html',
                error_msg="Method not allowed."
            )