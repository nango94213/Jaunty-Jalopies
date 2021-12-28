from datetime import datetime, timedelta
from operator import itemgetter

import psycopg2
from flask import request, render_template

from views.base import Base 
from sql_.sequel import SEQUEL
from utils import PSQL
from cmd_.default_values import DefaultValues

class Report(Base):
    """
    Will take care of all reports
    """

    def __init__(self, **kwargs):
        super(Report, self).__init__(**kwargs)

    def get_sales_by_color(self):

        def add_0_where_no_vehicle_color(results, existing_colors):
            found = [item['color'].lower() for item in results]
            for color in existing_colors:
                if color.lower() not in found:
                    results.append({"color": color, "count": "0"})

            return sorted(results, key=itemgetter('color'))

        if request.method in ['GET', 'POST']:

            data = {"title": "Report Sales By Color"}
        
            today = datetime.today()
            thirty_days_back = today - timedelta(30)
            thirty_days_back = thirty_days_back.strftime('%Y-%m-%d')

            one_year_back = today - timedelta(365)
            one_year_back = one_year_back.strftime('%Y-%m-%d')

            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    
                    # To get first sale date ever
                    cur.execute(SEQUEL.SELECT_ALL_SALES_BY_COLOR)
                    all_sales = cur.fetchall()                
                    first_sale_date = min([vehicle_color['minsaledate'] 
                        for vehicle_color in all_sales]) if all_sales and len(all_sales) else 'Day 1'
                    data['first_sale_date'] = first_sale_date

                    # To get all existing colors
                    cur.execute(SEQUEL.SELECT_ALL_EXISTING_COLORS)
                    all_existing_colors = cur.fetchall()   
                    all_existing_colors = [item['color'] for item in all_existing_colors] if all_existing_colors else []
                    existing_colors = list()
                    for item in DefaultValues.AVAILABLE_COLORS:
                        if item not in all_existing_colors:
                            existing_colors.append(item)
                    existing_colors.extend(all_existing_colors)

                    if request.method == 'GET':
                        # Select all sales by color
                        cur.execute(SEQUEL.SELECT_SALES_BY_COLOR.format(
                            initial_date=thirty_days_back
                        ))
                        bulk_sales_by_color = cur.fetchall()

                        # Select colors that are repeated (for same VIN, colorrs count > 1)
                        # We will subtract these colors from all sales by color
                        cur.execute(SEQUEL.SELECT_COLORS_COUNTS_TO_SUBTRACT.format(
                            initial_date=thirty_days_back
                        ))
                        color_counts_to_subtract = cur.fetchall()
                        color_counts_to_subtract = {item['color']: int(item['count']) for item in color_counts_to_subtract}

                        # Finally, select DISTINCT count of VINs in color table to identify multiple colors
                        # This will be added to final result of colors
                        cur.execute(SEQUEL.SELECT_MULTIPLE_COLORS_SALES.format(
                            initial_date=thirty_days_back
                        ))
                        multiple_color_sales = cur.fetchall()

                        # Merge results:
                        sales_by_color = list()
                        for item in bulk_sales_by_color:
                            if item['color'] in color_counts_to_subtract:
                                sales_by_color.append({"color": item['color'], "count": str(int(item['count']) - color_counts_to_subtract[item['color']])})
                            else:
                                sales_by_color.append({"color": item['color'], "count": item['count']})

                        if multiple_color_sales:
                            sales_by_color.append({"color": "Multiple", "count": multiple_color_sales[0]['count']})

                        data['results_thirty_days_back'] = add_0_where_no_vehicle_color(sales_by_color, existing_colors)

                    if request.method == 'POST':
                        if request.form.get('30days'):
                            cur.execute(SEQUEL.SELECT_SALES_BY_COLOR.format(
                                initial_date=thirty_days_back
                            ))
                            bulk_sales_by_color = cur.fetchall()

                            cur.execute(SEQUEL.SELECT_COLORS_COUNTS_TO_SUBTRACT.format(
                                initial_date=thirty_days_back
                            ))
                            color_counts_to_subtract = cur.fetchall()
                            color_counts_to_subtract = {item['color']: int(item['count']) for item in color_counts_to_subtract}

                            cur.execute(SEQUEL.SELECT_MULTIPLE_COLORS_SALES.format(
                                initial_date=thirty_days_back
                            ))
                            multiple_color_sales = cur.fetchall()

                            # Merge results:
                            sales_by_color = list()
                            for item in bulk_sales_by_color:
                                if item['color'] in color_counts_to_subtract:
                                    sales_by_color.append({"color": item['color'], "count": str(int(item['count']) - color_counts_to_subtract[item['color']])})
                                else:
                                    sales_by_color.append({"color": item['color'], "count": item['count']})

                            if multiple_color_sales:
                                sales_by_color.append({"color": "Multiple", "count": multiple_color_sales[0]['count']})

                            data['results_thirty_days_back'] = add_0_where_no_vehicle_color(sales_by_color, existing_colors)
                        
                        if request.form.get('1year'):

                            cur.execute(SEQUEL.SELECT_SALES_BY_COLOR.format(
                                initial_date=one_year_back
                            ))
                            bulk_sales_by_color = cur.fetchall()

                            cur.execute(SEQUEL.SELECT_COLORS_COUNTS_TO_SUBTRACT.format(
                                initial_date=one_year_back
                            ))
                            color_counts_to_subtract = cur.fetchall()
                            color_counts_to_subtract = {item['color']: int(item['count']) for item in color_counts_to_subtract}

                            cur.execute(SEQUEL.SELECT_MULTIPLE_COLORS_SALES.format(
                                initial_date=one_year_back
                            ))
                            multiple_color_sales = cur.fetchall()

                            # Merge results:
                            sales_by_color = list()
                            for item in bulk_sales_by_color:
                                if item['color'] in color_counts_to_subtract:
                                    sales_by_color.append({"color": item['color'], "count": str(int(item['count']) - color_counts_to_subtract[item['color']])})
                                else:
                                    sales_by_color.append({"color": item['color'], "count": item['count']})

                            if multiple_color_sales:
                                sales_by_color.append({"color": "Multiple", "count": multiple_color_sales[0]['count']})

                            data['results_one_year_back'] = add_0_where_no_vehicle_color(sales_by_color, existing_colors)
                        if request.form.get('day1'):
                            bulk_sales_by_color = all_sales

                            cur.execute(SEQUEL.SELECT_ALL_COLORS_COUNTS_TO_SUBTRACT)
                            color_counts_to_subtract = cur.fetchall()
                            color_counts_to_subtract = {item['color']: int(item['count']) for item in color_counts_to_subtract}

                            cur.execute(SEQUEL.SELECT_ALL_MULTIPLE_COLORS_SALES)
                            multiple_color_sales = cur.fetchall()

                            # Merge results:
                            sales_by_color = list()
                            for item in bulk_sales_by_color:
                                if item['color'] in color_counts_to_subtract:
                                    sales_by_color.append({"color": item['color'], "count": str(int(item['count']) - color_counts_to_subtract[item['color']])})
                                else:
                                    sales_by_color.append({"color": item['color'], "count": item['count']})

                            if multiple_color_sales:
                                sales_by_color.append({"color": "Multiple", "count": multiple_color_sales[0]['count']})

                            data['results_all_sales'] = add_0_where_no_vehicle_color(sales_by_color, existing_colors)

            return render_template('reportSalesByColor.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")

    def get_sales_by_type(self):

        def add_0_where_no_vehicle_type(results):
            found = [item['type'].lower() for item in results]
            for vehicle_type in DefaultValues.AVAILABLE_VEHICLE_TYPES:
                if vehicle_type.lower() not in found:
                    results.append({"type": vehicle_type, "count": "0"})

            return sorted(results, key=itemgetter('type'))
        

        if request.method in ['GET', 'POST']:

            data = {"title": "Report Sales By Type"}

            today = datetime.today()
            thirty_days_back = today - timedelta(30)
            thirty_days_back = thirty_days_back.strftime('%Y-%m-%d')

            one_year_back = today - timedelta(365)
            one_year_back = one_year_back.strftime('%Y-%m-%d')

            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(SEQUEL.SELECT_ALL_SALES_BY_TYPE)
                    all_sales = cur.fetchall()                
                    first_sale_date = min([vehicle_type['saledate'] 
                        for vehicle_type in all_sales]) if all_sales and len(all_sales) else 'Day 1'
                    data['first_sale_date'] = first_sale_date

                    if request.method == 'GET':
                        cur.execute(SEQUEL.SELECT_SALES_BY_TYPE.format(
                            initial_date=thirty_days_back
                        ))
                        data['results_thirty_days_back'] = add_0_where_no_vehicle_type(list(cur.fetchall()))

                    if request.method == 'POST':
                        if request.form.get('30days'):
                            cur.execute(SEQUEL.SELECT_SALES_BY_TYPE.format(
                                initial_date=thirty_days_back
                            ))
                            data['results_thirty_days_back'] = add_0_where_no_vehicle_type(cur.fetchall())
                        
                        if request.form.get('1year'):
                            cur.execute(SEQUEL.SELECT_SALES_BY_TYPE.format(
                                initial_date=one_year_back
                            ))
                            data['results_one_year_back'] = add_0_where_no_vehicle_type(cur.fetchall())
                        if request.form.get('day1'):
                            data['results_all_sales'] = add_0_where_no_vehicle_type(list(all_sales))

            return render_template('reportSalesByType.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")

    def get_sales_by_manufacturer(self):

        if request.method in ['GET', 'POST']:

            data = {"title": "Report Sales By Manufacturer"}

            today = datetime.today()
            thirty_days_back = today - timedelta(30)
            thirty_days_back = thirty_days_back.strftime('%Y-%m-%d')

            one_year_back = today - timedelta(365)
            one_year_back = one_year_back.strftime('%Y-%m-%d')

            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(SEQUEL.SELECT_ALL_SALES_BY_MANUFACTURER)
                    all_sales = cur.fetchall()                
                    first_sale_date = min([vehicle_type['saledate'] 
                        for vehicle_type in all_sales]) if all_sales and len(all_sales) else 'Day 1'
                    data['first_sale_date'] = first_sale_date

                    if request.method == 'GET':
                        cur.execute(SEQUEL.SELECT_SALES_BY_MANUFACTURER.format(
                            initial_date=thirty_days_back
                        ))
                        data['results_thirty_days_back'] = list(cur.fetchall())

                    if request.method == 'POST':
                        if request.form.get('30days'):
                            cur.execute(SEQUEL.SELECT_SALES_BY_MANUFACTURER.format(
                                initial_date=thirty_days_back
                            ))
                            data['results_thirty_days_back'] = cur.fetchall()
                        
                        if request.form.get('1year'):
                            cur.execute(SEQUEL.SELECT_SALES_BY_MANUFACTURER.format(
                                initial_date=one_year_back
                            ))
                            data['results_one_year_back'] = cur.fetchall()
                        if request.form.get('day1'):
                            data['results_all_sales'] = list(all_sales)
            return render_template('reportSalesByManufacturer.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
        
    def get_gross_customer_income(self):
        if request.method == 'GET':
            data = {"title": "Report Gross Customer Income"}
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                    customer_id = request.args.get('customer_id')
                    if customer_id:
                        data['results'] = dict()

                        cur.execute(SEQUEL.SELECT_GROSS_INCOME_BY_CUSTOMER_SALE.format(customer_id=customer_id))
                        data['results']['sales'] = list(cur.fetchall())

                        cur.execute(SEQUEL.SELECT_GROSS_INCOME_BY_CUSTOMER_REPAIR.format(customer_id=customer_id))
                        repairs_results = list()
                        for result in list(cur.fetchall()):
                            temp = dict(result)
                            temp['total_repair_cost'] = "{:.2f}".format(float(temp.get('total_repair_cost') or 0))
                            temp['total_part_cost'] = "{:.2f}".format(float(temp.get('total_part_cost') or 0))
                            repairs_results.append(temp)
                        data['results']['repairs'] = repairs_results
                        data['drill_down'] = True
                    else:
                        cur.execute(SEQUEL.SELECT_GROSS_INCOME_BY_CUSTOMER) 
                        results = list()
                        for result in list(cur.fetchall()):
                            temp = dict(result)
                            temp['gross_income'] = "{:.2f}".format(float(temp.get('gross_income') or 0))
                            results.append(temp)
                           
                        data['results'] = results

            return render_template('reportGrossCustomerIncome.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
        
    def get_repairs_by_manufacturer_type_model(self):
        if request.method == 'GET':
            data = {"title": "Report Repairs by Manufacturer/Type/Model"}
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                    manufacturer_name = request.args.get('manufacturer_name')
                    if manufacturer_name:
                        cur.execute(SEQUEL.SELECT_REPAIR_MF_TYPE.format(
                            manufacturer_name=manufacturer_name
                        ))
                        results = list()
                        for result in list(cur.fetchall()):
                            temp = dict(result)
                            temp['total_labor_charges'] = "{:.2f}".format(float(temp.get('total_labor_charges') or 0))
                            temp['total_part_cost'] = "{:.2f}".format(float(temp.get('total_part_cost') or 0))
                            temp['total_repair_cost'] = "{:.2f}".format(float(temp.get('total_repair_cost') or 0))
                            results.append(temp)
                        data['drill_down'] = results
                        data['manufacturer'] = manufacturer_name
                    else:
                        cur.execute(SEQUEL.SELECT_REPAIR_MF)    
                        results = list()
                        for result in list(cur.fetchall()):
                            temp = dict(result)
                            temp['total_labor_charges'] = "{:.2f}".format(float(temp.get('total_labor_charges') or 0))
                            temp['total_part_cost'] = "{:.2f}".format(float(temp.get('total_part_cost') or 0))
                            temp['total_repair_cost'] = "{:.2f}".format(float(temp.get('total_repair_cost') or 0))
                            results.append(temp)
                        data['results'] = results

            return render_template('reportRepairsByManTypeModel.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
       
    def get_below_cost_sales(self):
        if request.method == 'GET':
            data = {"title": "Report Below Cost Sales"}
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(SEQUEL.SELECT_BELOW_COST_SALES)    
                    results = list(cur.fetchall())

                    final_results = list()
                    for item in results:
                        final_results.append(item)
                        if float(item['price_ratio'].strip().split('%')[0]) <= 95:
                            final_results[-1]['class'] = 'bg-danger text-light'
                        else:
                            final_results[-1]['class'] = 'no-effect'

                    data['results'] = final_results
            return render_template('reportBelowCostSales.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
        
    def get_avg_time_in_inventory(self):
        if request.method == 'GET':
            data = {"title": "Report Avg Time in Inventory"}
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(SEQUEL.SELECT_AVG_TIME_INVENTORY)    
                    results = list(cur.fetchall())

                    final_results = list()
                    for item in results:
                        if item['average_time']:
                            final_results.append({'type': item['type'], 'average_time': int(item['average_time'])})
                        else:
                            final_results.append({'type': item['type'], 'average_time': 'N/A'})

                    data['results'] = final_results
            return render_template('reportAverageTimeInInventory.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
     
    def get_parts_statistics(self):
        if request.method == 'GET':
            data = {"title": "Report Parts Statistics"}

            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(SEQUEL.SELECT_PARTS_QUANTITY_SUM_OF_PROD_QUANTITY_PRICE)    
                    vendors = list(cur.fetchall())

                # Necessary only to format 2nd place decimal.
                data['vendors'] = [
                    {
                        "vendorname": vendor["vendorname"],
                        "qty": vendor["qty"],
                        "dollar_amount": "{:.2f}".format(float(vendor["dollar_amount"]))
                    } 
                for vendor in vendors]

            return render_template('reportPartsStatistics.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
        
    def get_monthly_sales(self):
        if request.method == 'GET':
            data = {"title": "Report Monthly Sales"}
            with PSQL.get_DB_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

                    year = request.args.get('year')
                    month = request.args.get('month')

                    if year and month:
                        cur.execute(SEQUEL.SELECT_SALES_PERSON_BY_YEAR_MONTH.format(
                            year=year,
                            month=month
                        ))

                        results = list()
                        for item in list(cur.fetchall()):
                            temp = dict(item)
                            temp['total_sales_income'] = "{:.2f}".format(float(temp.get('total_sales_income') or 0))
                            results.append(temp)

                        data['results'] = results
                        data['drill_down'] = True
                    else:
                        cur.execute(SEQUEL.SELECT_SALES_BY_YEAR_MONTH)    
                        results = list(cur.fetchall())

                        final_results = list()
                        for item in results:
                            temp = dict(item)
                            temp['total_net_income'] = "{:.2f}".format(float(temp.get('total_net_income') or 0))
                            temp['total_sales_income'] = "{:.2f}".format(float(temp.get('total_sales_income') or 0))
                            final_results.append(temp)
                            if float(temp['price_ratio'].strip().split('%')[0]) >= 125:
                                final_results[-1]['class'] = 'bg-success text-light'
                            elif float(temp['price_ratio'].strip().split('%')[0]) <= 110:
                                final_results[-1]['class'] = 'bg-warning'
                            else:
                                final_results[-1]['class'] = 'no-effect'

                        data['results'] = final_results
            return render_template('reportMonthlySales.html', data=data)
        return render_template("errorPage.html", error_msg="Method Not Allowed.")
        
  