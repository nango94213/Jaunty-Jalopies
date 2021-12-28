from flask import request, render_template, flash, session, redirect, url_for
import psycopg2

from views.base import Base 
from utils import PSQL

class Search(Base):

    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)

    def search(self):
        if request.method == 'GET':
            conn = PSQL.get_DB_connection()
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                count_cars_available_for_sale = self.get_count(cur)
                return render_template(
                    'searchPage.html', 
                    count_cars_available_for_sale=count_cars_available_for_sale
                )
        return render_template('searchPage.html')
