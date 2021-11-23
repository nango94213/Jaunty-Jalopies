from flask import request, render_template, flash, session, redirect, url_for

import psycopg2
from psycopg2 import sql

from views.base import Base 
from sql_.sequel import SEQUEL
from utils import PSQL, Hasher


class User(Base):
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def login(self):
        if request.method == 'GET':
            return render_template('loginForm.html', title="Login")
        elif request.method == 'POST':
            form_user = request.form['user_']
            form_password = request.form['password_'] 
            query_select_user = sql.SQL(SEQUEL.SELECT_USER)
            conn = PSQL.get_DB_connection()
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                users = PSQL.get_results(cur, query_select_user, attributes_tuple=(form_user,))
                if users:
                    if len(users) > 1:
                        flash(f"User '{form_user}' found multiple times in DB :/, please contact support", "danger")
                        return redirect("/login")
                    else:
                        if Hasher.check_hash(form_password, users[0]['password']) is True:
                            count_cars_available_for_sale = self.get_count(cur)
                            session['user'] = form_user
                            flash('Welcome back, ' + form_user + '.', 'success')
                            return render_template(
                                'searchPage.html', 
                                count_cars_available_for_sale=count_cars_available_for_sale
                            )
                        else:
                            flash("Sorry " + form_user + ", wrong password. :( ", "danger")
                            return render_template('loginForm.html', username=form_user)
            flash(f'User {form_user} not found :/', "danger")
            return redirect("/login")
    
    def logout(self):
        del session['user']
        return redirect('/')
