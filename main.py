from flask import Flask, session, request, redirect 

from conf.config import DEBUG, SECRET_KEY, PUBLIC_ACCESS_RESOURCES, RESET_DB
from views import User, Search, Vehicle, Sale, Report, Repair
from utils import LOG
from cmd_.initialize import reset_db

reset_db()

LOG.info("Initializing APP...")

app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.secret_key = SECRET_KEY

@app.before_request
def require_login():
    if not 'user' in session and not request.endpoint in PUBLIC_ACCESS_RESOURCES:
        return redirect("/")

app.add_url_rule('/', view_func=Search().search, methods=['POST', 'GET'])
app.add_url_rule('/login', view_func=User().login, methods=['POST', 'GET'])
app.add_url_rule('/logout', view_func=User().logout)
app.add_url_rule('/vehicle/<vin>', view_func=Vehicle().get_details, methods=['GET'])
app.add_url_rule('/vehicle', view_func=Vehicle().add_new, methods=['GET', 'POST'])
app.add_url_rule('/sell', view_func=Sale().sell, methods=['POST'])
app.add_url_rule('/repairs', view_func=Repair().show, methods=['GET', 'POST'])

app.add_url_rule('/reports/sales-by-color', view_func=Report().get_sales_by_color, methods=['GET', 'POST'])
app.add_url_rule('/reports/sales-by-type', view_func=Report().get_sales_by_type, methods=['GET', 'POST'])
app.add_url_rule('/reports/sales-by-manufacturer', view_func=Report().get_sales_by_manufacturer, methods=['GET', 'POST'])
app.add_url_rule('/reports/gross-customer-income', view_func=Report().get_gross_customer_income, methods=['GET', 'POST'])
app.add_url_rule('/reports/repairs-by-manufacturer-type-model', 
    view_func=Report().get_repairs_by_manufacturer_type_model, methods=['GET', 'POST'])
app.add_url_rule('/reports/below-cost-sales', view_func=Report().get_below_cost_sales, methods=['GET', 'POST'])
app.add_url_rule('/reports/avg-time-in-inventory', view_func=Report().get_avg_time_in_inventory, methods=['GET', 'POST'])
app.add_url_rule('/reports/parts-statistics', view_func=Report().get_parts_statistics, methods=['GET'])
app.add_url_rule('/reports/monthly-sales', view_func=Report().get_monthly_sales, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True, threaded=True)
