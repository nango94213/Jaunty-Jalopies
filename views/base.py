from sql_.sequel import SEQUEL
from utils import PSQL

class Base:

    def __init__(self):
        self.db = PSQL()

    def get_count(self, cur):
        query_count_cars_available_for_sale = SEQUEL.SELECT_COUNT_CARS_AVAILABLE_FOR_SALE
        count_cars_available_for_sale = PSQL.get_results(cur, query_count_cars_available_for_sale)
        if count_cars_available_for_sale:
            count_cars_available_for_sale = count_cars_available_for_sale[0]["count"]
        else:
            count_cars_available_for_sale = 0
        return count_cars_available_for_sale