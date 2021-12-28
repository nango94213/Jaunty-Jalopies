from collections import OrderedDict

import psycopg2

from sql_.sequel import SEQUEL
from utils import PSQL
from cmd_.default_values import DefaultValues

class Base:

    def __init__(self):
        self.db = PSQL()

    def get_unsold_cars_count(self, cur):
        count_unsold_cars = PSQL.get_results(cur, SEQUEL.SELECT_COUNT_UNSOLD_CARS)
        return count_unsold_cars[0]["count"] if count_unsold_cars else 0

    def get_all_manufacturers(self, cur):
        return PSQL.get_results(cur, SEQUEL.SELECT_ALL_MANUFACTURERS)

    def get_manufacturers_and_count_for_unsold_cars(self, cur):
        return PSQL.get_results(cur, SEQUEL.SELECT_MANUFACTURERS_AND_COUNT_OF_UNSOLD_CARS)

    def get_models_years_and_count(self, cur):
        return PSQL.get_results(cur, SEQUEL.SELECT_MODEL_YEAR_AND_COUNT_OF_UNSOLD_CARS)

    def get_colors_and_count_for_unsold_cars(self, cur):
        return PSQL.get_results(cur, SEQUEL.SELECT_COLORS_AND_COUNT_OF_UNSOLD_CARS)

    def get_vehicle_type_and_count_for_unsold_cars(self, cur):
        return PSQL.get_results(cur, SEQUEL.SELECT_VEHICLE_TYPES_AND_COUNT_OF_UNSOLD_CARS)

    def merge_items_and_counts(
        self, items_of_unsold_cars, all_items, targeted_column):
        """
        Will return a dict with the item and the count to be used in Bootstrap.
        """
        results = dict()
        for item in items_of_unsold_cars:
            results[item[targeted_column]] = f" ({item['count']})"
        
        for item in all_items:
            if item[targeted_column] not in results:
                results[item[targeted_column]] = ''
        
        # return ordered dictionary by key
        return OrderedDict(sorted(results.items()))

    def merge_db_vs_list_items_and_counts(
        self, db_items, items, targeted_column):
        """
        Will return a dict with the item and the count to be used in Bootstrap.
        This method takes in a fetchall result from DB and a list from Python.
        """
        results = dict()
        for db_item in db_items:
            results[db_item[targeted_column]] = f" ({db_item['count']})"
        
        for item in items:
            if item not in results:
                results[item] = ''
        
        # return ordered dictionary by key
        return OrderedDict(sorted(results.items()))

    def merge_colors_and_counts(
        self, colors_of_unsold_cars, all_colors):
        return self.merge_db_vs_list_items_and_counts(
            colors_of_unsold_cars, all_colors, 'color'
        )

    def merge_vehicle_types_and_counts(
        self, vehicle_types_of_unsold_cars, all_vehicle_types):
        return self.merge_db_vs_list_items_and_counts(
            vehicle_types_of_unsold_cars, all_vehicle_types, 'type'
        )

    def generate_and_merge_range_model_year_counts(self, db_dates_and_count):
        """
        Will take min and max years from input, 
        will create range and will indicate count.
        """
        if db_dates_and_count:
            results = dict()
            helper = list()
            for db_item in db_dates_and_count:
                helper.append(int(db_item['year']))
                results[db_item['year']] = f" ({db_item['count']})"
            min_ = min(helper)
            max_ = max(helper)

            for item in range(min_,max_):
                if item not in results:
                    results[item] = ''

            # return ordered dictionary by key
            return OrderedDict(sorted(results.items()))

        return dict()

    def refresh_data(self):
        with PSQL.get_DB_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(SEQUEL.SELECT_DISTINCT_VEHICLE_TYPES)
                self.vehicle_types = list()
                for vehicle_type in cur.fetchall():
                    self.vehicle_types.append(vehicle_type['type'])

                cur.execute(SEQUEL.SELECT_MANUFACTURERS)
                self.manufacturers = list()
                for manufacturer in cur.fetchall():
                    self.manufacturers.append(manufacturer['mfname'])
        
        self.data = {
            "vehicle_types": self.vehicle_types,
            "manufacturers": self.manufacturers,
            "number_of_cup_holders": DefaultValues.NUMBER_OF_CUP_HOLDERS_OPTIONS,
            "drivetrain_types": DefaultValues.DRIVETRAIN_TYPE_OPTIONS,
            "back_seat_count": DefaultValues.BACK_SEAT_COUNT_OPTIONS,
            "roof_types": DefaultValues.ROOF_TYPE_OPTIONS,
            "number_of_doors": DefaultValues.NUMBER_OF_DOORS_OPTIONS,
            "cargo_cover_types": DefaultValues.CARGO_COVER_TYPE_OPTIONS,
            "no_rear_axles": DefaultValues.NO_REAR_AXLES_OPTIONS
        }