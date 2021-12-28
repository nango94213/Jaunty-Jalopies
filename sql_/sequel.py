
class SEQUEL:
    """
    Use:
    transaction = SEQUEL.INSERT_PRIVILEGED_USER.format(
        username=user['username'],
        password=user['password'],
        firstname=user['firstname'],
        lastname=user['lastname'],
        role=user['role']
    )
    cur.execute(transaction)
    insert_statement = f"INSERT_{user['role'].upper()}"
    transaction = getattr(SEQUEL, insert_statement).format(
        username=user['username']
    )
    cur.execute(transaction)
    """
    
    INSERT_PRIVILEGED_USER = """INSERT INTO PrivilegedUser 
                                VALUES ('{username}', '{password}', '{firstname}', '{lastname}', '{role}')"""
    
    INSERT_SERVICE_WRITER = """ INSERT INTO ServiceWriter 
                                VALUES ('{username}')"""
    
    INSERT_MANAGER = """INSERT INTO Manager 
                        VALUES ('{username}')"""
    
    INSERT_OWNER = """  INSERT INTO Owner 
                        VALUES ('{username}')"""
    
    INSERT_SALES_PERSON = """   INSERT INTO SalesPerson 
                                VALUES ('{username}')"""
    
    INSERT_INVENTORY_CLERK = """INSERT INTO InventoryClerk 
                                VALUES ('{username}')"""
    
    INSERT_OWNER = """  INSERT INTO Owner 
                        VALUES ('{username}');
                        INSERT INTO ServiceWriter
                        VALUES ('{username}');
                        INSERT INTO Manager
                        VALUES ('{username}');
                        INSERT INTO SalesPerson
                        VALUES ('{username}');
                        INSERT INTO InventoryClerk
                        VALUES ('{username}');"""

    INSERT_MANUFACTURER = """   INSERT INTO Manufacturer 
                                VALUES ('{name}')"""

    SELECT_USER = """   SELECT * FROM PrivilegedUser
                        WHERE username = %s;"""

    SELECT_COUNT_UNSOLD_CARS = """  SELECT COUNT(vin) FROM Vehicle
                                    WHERE vin NOT IN (
                                        SELECT vin FROM Vehicle_Sold_Customer
                                    );"""

    SELECT_ALL_MANUFACTURERS = "SELECT * FROM Manufacturer;"

    SELECT_MANUFACTURERS_AND_COUNT_OF_UNSOLD_CARS = """ SELECT DISTINCT MFName, count(MFName) FROM Vehicle
                                                        WHERE vin NOT IN (
                                                            SELECT vin FROM Vehicle_Sold_Customer
                                                        )
                                                        GROUP BY MFName;"""

    SELECT_COLORS_AND_COUNT_OF_UNSOLD_CARS = """SELECT DISTINCT Color, count(Color) FROM Vehicle
                                                NATURAL JOIN Vehicle_Color
                                                WHERE vin NOT IN (
                                                    SELECT vin FROM Vehicle_Sold_Customer
                                                )
                                                GROUP BY Color;"""

    SELECT_VEHICLE_TYPES_AND_COUNT_OF_UNSOLD_CARS = """ SELECT DISTINCT Type, count(Type) FROM Vehicle
                                                        WHERE vin NOT IN (
                                                            SELECT vin FROM Vehicle_Sold_Customer
                                                        )
                                                        GROUP BY Type;"""

    SELECT_MODEL_YEAR_AND_COUNT_OF_UNSOLD_CARS = """SELECT DISTINCT Year, count(Year) FROM Vehicle
                                                    WHERE vin NOT IN (
                                                        SELECT vin FROM Vehicle_Sold_Customer
                                                    )
                                                    GROUP BY Year;"""

    
    """
    # ============================================
    # SELECT_UNSOLD_VEHICLE_AND_COLORS examples
    # ============================================
    SELECT VIN, Type, Year, MFName, MName, color, InvoicePrice *1.25 AS ListPrice
    FROM Vehicle NATURAL JOIN Vehicle_Color
    WHERE Color = 'Black' 
    OR MFName = 'BMW' 
    OR Year = '2021' 
    OR Type = 'Convertible' 
    AND VIN NOT IN (
        SELECT vin FROM Vehicle_Sold_Customer
    );

    SELECT VIN, Type, Year, MFName, MName, color, InvoicePrice *1.25 FROM Vehicle NATURAL JOIN
    Vehicle_Color
    WHERE InvoicePrice *1.25 >= 40000 
    AND VIN NOT IN (
        SELECT vin FROM Vehicle_Sold_Customer
    );

    SELECT VIN, Type, Year, MFName, MName, color, InvoicePrice *1.25 AS ListPrice
    FROM Vehicle NATURAL JOIN
    Vehicle_Color
    WHERE MFName LIKE '%2021%'
    OR Year::VARCHAR LIKE '%2021%' 
    OR MName LIKE '%2021%' 
    OR Description LIKE '%2021%' 
    AND VIN NOT IN (
        SELECT vin FROM Vehicle_Sold_Customer
    );

    """
    SELECT_UNSOLD_VEHICLE_AND_COLORS = """  SELECT VIN, Type, Year, MFName, MName, color, InvoicePrice *1.25 AS ListPrice
                                            FROM Vehicle NATURAL JOIN
                                            Vehicle_Color
                                            WHERE {conditions}VIN NOT IN (
                                                SELECT vin FROM Vehicle_Sold_Customer
                                            );"""

    SELECT_SOLD_VEHICLE_AND_COLORS = """    SELECT VIN, Type, Year, MFName, MName, color, InvoicePrice *1.25 AS ListPrice
                                            FROM Vehicle NATURAL JOIN
                                            Vehicle_Color
                                            WHERE {conditions}VIN IN (
                                                SELECT vin FROM Vehicle_Sold_Customer
                                            );"""
    
    SELECT_ALL_VEHICLE_AND_COLORS = """ SELECT VIN, Type, Year, MFName, MName, color, InvoicePrice *1.25 AS ListPrice
                                        FROM Vehicle NATURAL JOIN
                                        Vehicle_Color
                                        WHERE {conditions}VIN IN (
                                            SELECT vin FROM Vehicle
                                        );"""

    SELECT_VEHICLE_BULK_DETAIL_INFO = """   SELECT VIN, Type, Year, MFName, MName, Description, color, InvoicePrice, 
                                            InvoicePrice *1.25 AS ListPrice, IClerkUserName, DateAdded,
                                            CONCAT(pu.firstname, ' ', pu.lastname) AS inventory_clerk_name
                                            FROM Vehicle v NATURAL JOIN
                                            Vehicle_Color vc
                                            JOIN PrivilegedUser pu
                                            ON pu.Username = v.IClerkUserName
                                            WHERE VIN = '{vin}';"""

    SELECT_VEHICLE_SALE_DETAILS = """   SELECT VIN, vsc.ID, SalesPersonUserName, SaleDate, 
                                        SoldPrice,
                                        CASE
                                            WHEN
                                                EXISTS (SELECT DriverLicenseNumber from Individual WHERE DriverLicenseNumber = ID) 
                                                THEN (SELECT CONCAT(
                                                    'name: [', Firstname, ' ', Lastname, '], address: [', Address, '], phone number: [', PhoneNumber, '], email: [', EmailAddress, ']') 
                                                    FROM Individual ind
                                                    JOIN Customer cu
                                                    ON ind.DriverLicenseNumber = cu.ID
                                                    WHERE ind.DriverLicenseNumber = vsc.ID) 
                                            WHEN 
                                                EXISTS (SELECT TIN from Business WHERE TIN = ID) 
                                                THEN (SELECT CONCAT(
                                                    'name: [', BName, '], address: [', Address, '], phone number: [', PhoneNumber, '], email: [', EmailAddress, ']') 
                                                    FROM Business busi
                                                    JOIN Customer cu
                                                    ON busi.TIN = cu.ID
                                                    WHERE busi.TIN = vsc.ID) 
                                            ELSE
                                                'Unknown'
                                        END AS Customer_Contact_Info,
                                        CONCAT(pu.firstname, ' ', pu.lastname) AS sales_person_name
                                        FROM Vehicle_Sold_Customer vsc
                                        JOIN PrivilegedUser pu
                                        ON vsc.SalesPersonUserName = pu.username
                                        WHERE VIN = '{vin}';"""

    # ============================================
    # SELECT_REPAIRS_DETAILS example
    # ============================================
    """ 
    SELECT VIN, CustomerID, ServiceWriterUsername, StartDate, 
    COALESCE(CompletionDate::text, 'In Progress') AS CompletionDate, 
    SUM(p.Quantity * p.Price) AS Parts_Total,
    LaborCharges,
    CASE
        WHEN
            EXISTS (SELECT DriverLicenseNumber from Individual WHERE DriverLicenseNumber = '869-87-9830') 
            THEN (SELECT CONCAT(Firstname, ' ', Lastname) from Individual WHERE DriverLicenseNumber = '869-87-9830') 
        WHEN 
            EXISTS (SELECT TIN from Business WHERE TIN = '869-87-9830') 
            THEN (SELECT BName from Business WHERE TIN = '869-87-9830') 
        ELSE
            'Unknown'
    END AS Customer_Name
    FROM Repair r
    NATURAL JOIN Part p
    JOIN Customer c ON
    r.CustomerID = c.ID
    GROUP BY (VIN, StartDate, CustomerID)
    HAVING VIN = '9C2KE02007R001317';
    """
    SELECT_REPAIRS_DETAILS =""" SELECT VIN, CustomerID, ServiceWriterUsername, StartDate, 
                                COALESCE(CompletionDate::text, 'In Progress') AS CompletionDate, 
                                SUM(p.Quantity * p.Price) AS Parts_Total,
                                LaborCharges,
                                CASE
                                    WHEN
                                        EXISTS (SELECT DriverLicenseNumber from Individual WHERE DriverLicenseNumber = CustomerID) 
                                        THEN (SELECT CONCAT(Firstname, ' ', Lastname) from Individual WHERE DriverLicenseNumber = CustomerID) 
                                    WHEN 
                                        EXISTS (SELECT TIN from Business WHERE TIN = CustomerID) 
                                        THEN (SELECT BName from Business WHERE TIN = CustomerID) 
                                    ELSE
                                        'Unknown'
                                END AS Customer_Name,
                                CONCAT(pu.firstname, ' ', pu.lastname) AS service_writer_name
                                FROM Repair r
                                NATURAL LEFT JOIN Part p
                                JOIN Customer c ON
                                r.CustomerID = c.ID
                                JOIN PrivilegedUser pu
                                ON r.ServiceWriterUsername = pu.username
                                GROUP BY (VIN, StartDate, CustomerID, pu.firstname, pu.lastname)
                                HAVING VIN = '{vin}';"""

    SELECT_ALL_INFO_FOR_REPAIR =""" SELECT v.VIN, v.Description, v.MName, v.Year, v.MFName, v.Type,
                                    c.ID, c.Address, c.PhoneNumber, c.EmailAddress,
                                    i.Firstname, i.Lastname,
                                    b.BName, b.PCName, b.Title,
                                    r.RDescription, r.OdometerReading, r.LaborCharges, r.StartDate
                                    FROM Vehicle v
                                    NATURAL JOIN Repair r
                                    JOIN Customer c 
                                    ON r.CustomerID = c.ID
                                    LEFT JOIN Individual i
                                    ON c.ID = i.DriverLicenseNumber
                                    LEFT JOIN Business b
                                    ON c.ID = b.TIN
                                    WHERE CompletionDate IS NULL 
                                    AND VIN = '{vin}';"""

    SELECT_ONLY_VEHICLE_AND_COLOR = """ SELECT VIN, color
                                        FROM Vehicle_Color
                                        WHERE {conditions}VIN NOT IN (
                                            SELECT vin FROM Vehicle_Sold_Customer
                                        );"""
    
    SELECT_ONLY_VEHICLE_AND_COLOR_IMPROVED = """SELECT VIN, STRING_AGG(Color, ', ') AS Colors
                                                FROM Vehicle_Color
                                                GROUP BY VIN
                                                HAVING VIN = '{vin}'
                                                ORDER BY VIN;"""

    IS_CUSTOMER_INDIVIDUAL = "SELECT EXISTS (SELECT DriverLicenseNumber FROM Individual WHERE DriverLicenseNumber = '{id_}');"

    IS_CUSTOMER_BUSINESS = "SELECT EXISTS (SELECT TIN FROM Business WHERE TIN = '{id_}');"
    
    SELECT_ATTRIBUTES_FROM_VEHICLE_TYPE = "SELECT * FROM {vehicle_type} WHERE VIN = '{vin}';"

    SELECT_DISTINCT_VEHICLE_TYPES = "SELECT DISTINCT(Type) FROM Vehicle ORDER BY Type;"

    SELECT_MANUFACTURERS = "SELECT MFName FROM Manufacturer ORDER BY MFName;"

    EXISTS_VIN = "SELECT EXISTS (SELECT VIN FROM Vehicle WHERE VIN = '{vin}');"

    INSERT_DATA_SUV = """   INSERT INTO Vehicle 
                            VALUES ('{vin}', '{description}', '{invoice_price}', '{type}', 
                            '{model_year}', '{model_name}', '{date_added}', '{clerk_username}', 
                            '{manufacturer_name}');
                            INSERT INTO SUV VALUES ('{vin}', '{number_of_cup_holders}', '{drivetrain_type}');
                            {insert_statement_colors}"""
    
    INSERT_DATA_CONVERTIBLE = """   INSERT INTO Vehicle 
                                    VALUES ('{vin}', '{description}', '{invoice_price}', '{type}', 
                                    '{model_year}', '{model_name}', '{date_added}', '{clerk_username}', 
                                    '{manufacturer_name}');
                                    INSERT INTO Convertible VALUES ('{vin}', '{back_seat_count}', '{roof_type}');
                                    {insert_statement_colors}"""

    INSERT_DATA_CAR = """   INSERT INTO Vehicle 
                            VALUES ('{vin}', '{description}', '{invoice_price}', '{type}', 
                            '{model_year}', '{model_name}', '{date_added}', '{clerk_username}', 
                            '{manufacturer_name}');
                            INSERT INTO Car VALUES ('{vin}', '{number_of_doors}');
                            {insert_statement_colors}"""

    INSERT_DATA_VAN = """   INSERT INTO Vehicle 
                            VALUES ('{vin}', '{description}', '{invoice_price}', '{type}', 
                            '{model_year}', '{model_name}', '{date_added}', '{clerk_username}', 
                            '{manufacturer_name}');
                            INSERT INTO Van VALUES ('{vin}', {has_driver_side_backdoor});
                            {insert_statement_colors}"""

    INSERT_DATA_TRUCK = """ INSERT INTO Vehicle 
                            VALUES ('{vin}', '{description}', '{invoice_price}', '{type}', 
                            '{model_year}', '{model_name}', '{date_added}', '{clerk_username}', 
                            '{manufacturer_name}');
                            INSERT INTO Truck VALUES ('{vin}', '{cargo_capacity}', '{cargo_cover_type}', '{no_rear_axles}');
                            {insert_statement_colors}"""

    SELECT_INDIVIDUAL_CUSTOMER = """SELECT * FROM Customer c
                                    JOIN Individual i 
                                    ON c.ID = i.DriverLicenseNumber
                                    WHERE ID = '{customerID}';"""

    SELECT_BUSINESS_CUSTOMER = """  SELECT * FROM Customer c
                                    JOIN Business b
                                    ON c.ID = b.TIN
                                    WHERE ID = '{customerID}';"""

    SELL_VEHICLE = """  INSERT INTO Vehicle_Sold_Customer 
                        VALUES ('{vin}', '{id}', '{sales_person_username}', '{sale_date}', '{sold_price}');"""

    SELECT_SALES_BY_TYPE = """  SELECT DISTINCT(Type), count(Type) AS count
                                FROM Vehicle
                                NATURAL JOIN Vehicle_Sold_Customer
                                WHERE SaleDate >= '{initial_date}'
                                GROUP BY Type
                                ORDER BY Type;"""

    SELECT_ALL_SALES_BY_TYPE = """  SELECT DISTINCT(Type), count(Type) AS count, min(SaleDate) AS saleDate
                                    FROM Vehicle
                                    NATURAL JOIN Vehicle_Sold_Customer
                                    GROUP BY Type
                                    ORDER BY Type;"""

    SELECT_ALL_EXISTING_COLORS = "SELECT DISTINCT Color FROM Vehicle_Color;"

    SELECT_ALL_SALES_BY_COLOR = """ SELECT Color, Count(Color) AS count, min(SaleDate) AS minSaleDate
                                    FROM Vehicle_Sold_Customer vsc
                                    NATURAL JOIN
                                    Vehicle_Color
                                    GROUP BY Color
                                    ORDER BY Color;"""
    
    SELECT_SALES_BY_COLOR = """ SELECT Color, Count(Color) AS count, min(SaleDate) AS minSaleDate
                                FROM Vehicle_Sold_Customer vsc
                                NATURAL JOIN
                                Vehicle_Color
                                WHERE vsc.saleDate > '{initial_date}'
                                GROUP BY Color
                                ORDER BY Color;"""

    SELECT_ALL_COLORS_COUNTS_TO_SUBTRACT = """  SELECT Color, Count(Color) FROM Vehicle_Color 
                                                WHERE VIN IN (
                                                    SELECT VIN
                                                    FROM Vehicle_Sold_Customer vsc
                                                    NATURAL JOIN Vehicle_Color
                                                    GROUP BY VIN
                                                    HAVING count(VIN) > 1
                                                )
                                                GROUP BY Color
                                                ORDER BY Color;"""

    SELECT_COLORS_COUNTS_TO_SUBTRACT = """  SELECT Color, Count(Color) FROM Vehicle_Color 
                                            WHERE VIN IN (
                                                SELECT VIN
                                                FROM Vehicle_Sold_Customer vsc
                                                NATURAL JOIN Vehicle_Color
                                                WHERE vsc.saleDate > '{initial_date}'
                                                GROUP BY VIN
                                                HAVING count(VIN) > 1
                                            )
                                            GROUP BY Color
                                            ORDER BY Color;"""

    SELECT_ALL_MULTIPLE_COLORS_SALES = """  SELECT count(DISTINCT(VIN))
                                            FROM Vehicle_Sold_Customer vsc
                                            NATURAL JOIN Vehicle_Color
                                            GROUP BY VIN
                                            HAVING count(VIN) > 1;"""

    SELECT_MULTIPLE_COLORS_SALES = """  SELECT count(DISTINCT(VIN))
                                            FROM Vehicle_Sold_Customer vsc
                                            NATURAL JOIN Vehicle_Color
                                            WHERE vsc.saleDate > '{initial_date}'
                                            GROUP BY VIN
                                            HAVING count(VIN) > 1;"""

    SELECT_SALES_BY_MANUFACTURER = """  SELECT DISTINCT(MFName), count(MFName) AS count
                                        FROM Vehicle 
                                        NATURAL JOIN Vehicle_Sold_Customer
                                        WHERE SaleDate >= '{initial_date}'
                                        GROUP BY MFName
                                        ORDER BY MFName;"""

    SELECT_ALL_SALES_BY_MANUFACTURER = """  SELECT DISTINCT(MFName), count(MFName) AS count, min(SaleDate) AS saleDate
                                            FROM Vehicle
                                            NATURAL JOIN Vehicle_Sold_Customer
                                            GROUP BY MFName
                                            ORDER BY MFName;"""

    SELECT_PARTS_QUANTITY_SUM_OF_PROD_QUANTITY_PRICE = """  SELECT VendorName, sum(Quantity) as qty, sum(Price*Quantity) as dollar_amount
                                                            FROM Part
                                                            GROUP BY VendorName
                                                            ORDER BY VendorName;"""

    EXISTS_CUSTOMER_ID = "SELECT EXISTS (SELECT ID FROM Customer WHERE ID = '{customer_id}');"

    INSERT_DATA_INDIVIDUAL = """INSERT INTO Customer 
                                VALUES ('{id}', '{address}', '{phone_number}', '{email_address}');
                                INSERT INTO Individual VALUES ('{driver_license_number}', '{firstname}', '{lastname}');"""

    INSERT_DATA_BUSINESS = """  INSERT INTO Customer 
                                VALUES ('{id}', '{address}', '{phone_number}', '{email_address}');
                                INSERT INTO Business VALUES ('{tin}', '{business_name}', '{primary_contact_name}', '{primary_contact_title}');"""

    SELECT_SOLD_VEHICLE_AND_COLORS_IMPROVED = """   SELECT VIN, Type, Description, Year, MFName, MName, STRING_AGG(color, ', ') AS Color, InvoicePrice *1.25 AS ListPrice
                                                    FROM Vehicle NATURAL JOIN
                                                    Vehicle_Color
                                                    WHERE VIN IN (
                                                        SELECT vin FROM Vehicle_Sold_Customer
                                                    ) AND VIN='{vin}'
                                                    GROUP BY VIN;"""

    EXISTS_REPAIR_FOR_VIN = "SELECT EXISTS (SELECT VIN FROM Repair WHERE CompletionDate IS NULL AND VIN = '{vin}');"

    INSERT_INTO_REPAIR = """INSERT INTO Repair 
                            VALUES ('{vin}', '{customer_id}', '{start_date}', '{service_writer_username}', 
                            '{repair_description}', NULL, '{odometer_reading}', '0');"""

    INSERT_COMPLETED_REPAIR = """INSERT INTO Repair 
                            VALUES ('{vin}', '{customer_id}', '{start_date}', '{service_writer_username}', 
                            '{repair_description}', '{completion_date}', '{odometer_reading}', '{labor_charges}');"""

    SELECT_REPAIR = """ SELECT * 
                        FROM Repair
                        WHERE VIN = '{vin}'
                        AND CustomerID = '{customer_id}'
                        AND StartDate = '{start_date}';"""

    UPDATE_REPAIR_LABOR_CHARGES = """   UPDATE Repair
                                        SET LaborCharges = '{new_labor_charges}'
                                        WHERE VIN = '{vin}'
                                        AND CustomerID = '{customer_id}'
                                        AND StartDate = '{start_date}';"""

    COMPLETE_REPAIR = """   UPDATE Repair
                            SET CompletionDate = '{completion_date}'
                            WHERE VIN = '{vin}'
                            AND CustomerID = '{customer_id}'
                            AND StartDate = '{start_date}';"""

    SELECT_PARTS = """  SELECT PartNumber AS part_number,
                        VendorName AS vendor_name,
                        Quantity as quantity,
                        Price as unit_price
                        FROM Part
                        WHERE VIN = '{vin}'
                        AND CustomerID = '{customer_id}'
                        AND StartDate = '{start_date}';"""
    
    INSERT_INTO_PARTS = """ INSERT INTO Part 
                            VALUES ('{vin}', '{customer_id}', '{start_date}', '{part_number}', 
                            '{vendor_name}', '{quantity}', '{price}');"""

    EXISTS_PART = """   SELECT EXISTS ( SELECT PartNumber 
                                        FROM Part 
                                        WHERE VIN = '{vin}'
                                        AND CustomerId = '{customer_id}'
                                        AND StartDate = '{start_date}' 
                                        AND PartNumber = '{part_number}'
                                        AND VendorName = '{vendor_name}'
                                        AND Price = '{price}');"""

    DELETE_PART = """   DELETE FROM Part
                        WHERE VIN = '{vin}'
                        AND CustomerId = '{customer_id}'
                        AND StartDate = '{start_date}' 
                        AND PartNumber = '{part_number}'
                        AND VendorName = '{vendor_name}'
                        AND Price = '{price}';"""   

    # sql for AverageTime Report
    SELECT_AVG_TIME_INVENTORY = """ SELECT v.type, AVG(s.saledate - v.dateadded) average_time 
                                    FROM Vehicle v
                                    LEFT JOIN vehicle_sold_customer s
                                    ON v.vin=s.vin
                                    GROUP BY v.type
                                    ORDER BY v.type;"""

    #sql for Below Cost Sales Report
    SELECT_BELOW_COST_SALES = """   SELECT s.saledate, v.invoiceprice, s.soldprice, 
                                    CONCAT(s.firstname, ' ',s.lastname) salesperson, 
                                    TO_CHAR(100*(s.soldprice/v.invoiceprice),'999D99%') price_ratio, 
                                    CASE
                                        WHEN i.driverlicensenumber IS NOT NULL THEN CONCAT(i.firstname, ' ', i.lastname)
                                        ELSE b.bname
                                    END AS name
                                    FROM (SELECT * FROM vehicle_sold_customer a INNER JOIN privilegeduser b on a.salespersonusername=b.username) s
                                    LEFT JOIN Vehicle v
                                    ON s.vin=v.vin
                                    LEFT JOIN Individual i
                                    ON s.id = i.driverlicensenumber
                                    LEFT JOIN Business b
                                    ON s.id = b.tin
                                    WHERE v.invoiceprice > s.soldprice
                                    ORDER by s.saledate DESC, price_ratio DESC;"""

    # sql for month sale report
    SELECT_SALES_BY_YEAR_MONTH ="""  SELECT extract(year from saledate) as years,
                                extract(month from saledate) as months,
                                sum(s.soldprice-v.invoiceprice) as total_net_income,
                                sum(s.soldprice) as total_sales_income, 
                                count(distinct s.vin) as total_number_sold, 
                                to_char(100.0*AVG(s.soldprice/v.invoiceprice),'999D99%') as price_ratio
                                FROM vehicle_sold_customer s
                                NATURAL JOIN vehicle v
                                group by years, months
                                order by years desc, months desc;"""
    
    # sql for month sale report drill down
    SELECT_SALES_PERSON_BY_YEAR_MONTH = """ SELECT sum(s.soldprice) total_sales_income, 
                                            count(distinct s.vin) total_number_sold,
                                            concat(p.firstname,' ',p.lastname) fullname
                                            FROM vehicle_sold_customer s
                                            INNER JOIN Vehicle v
                                            on s.vin=v.vin
                                            INNER JOIN PrivilegedUser p
                                            on s.salespersonusername=p.username
                                            where extract(month from saledate) = '{month}'
                                            AND extract(year from saledate) = '{year}'
                                            group by fullname
                                            order by total_number_sold desc, total_sales_income desc ;"""

    # sql for Gross Customer Income
    SELECT_GROSS_INCOME_BY_CUSTOMER = """
    SELECT f.number_sale,f.number_repair,f.id,f.first_date,f.last_date,f.gross_income,
    CASE
        WHEN i.driverlicensenumber is not null then concat(i.firstname,' ',i.lastname)
        ELSE b.bname
    END AS name
    FROM (select count(distinct s.vin) number_sale, count(rr.vin) number_repair, CASE
        WHEN min(rr.startdate) is null THEN min(s.saledate)
        WHEN min(rr.startdate) < min(s.saledate) THEN min(rr.startdate)
        else min(s.saledate)
    END AS first_date, CASE
        WHEN max(rr.startdate) is null THEN max(s.saledate)
        WHEN max(rr.startdate) > max(s.saledate) THEN max(rr.startdate)
        else max(s.saledate)
    END AS last_date,s.id, CASE
        WHEN sum(rr.total_repair_cost) is null THEN sum(s.soldprice)
        else (sum(s.soldprice)+sum(rr.total_repair_cost))
    END as gross_income
    from (select vin,id,soldprice,saledate from vehicle_sold_customer) s left join (select r.vin, r.startdate,CASE
        WHEN temp.total_part_cost is null THEN r.laborcharges
        WHEN temp.total_part_cost is not null THEN r.laborcharges+temp.total_part_cost
    END as total_repair_cost from Repair r left join (select vin,sum(quantity*price) as total_part_cost from part group by vin)temp on r.vin=temp.vin)rr on s.vin=rr.vin
    GROUP BY s.id
    ORDER BY gross_income DESC
    LIMIT 15) f
    LEFT JOIN Individual i
    ON f.id = i.driverlicensenumber
    LEFT JOIN Business b
    ON f.id = b.tin
    ORDER BY f.gross_income DESC,f.last_date DESC;"""

    # sql for Gross Customer Income drill down - sales
    SELECT_GROSS_INCOME_BY_CUSTOMER_SALE="""
    SELECT v.vin, v.year, v.mname model, v.mfname manufacturer, sold.saledate, concat(sold.firstname,' ',sold.lastname) salesperson, sold.soldprice
    FROM Vehicle v INNER JOIN (select * from vehicle_sold_customer a inner join privilegeduser b on a.salespersonusername=b.username) sold
    ON v.vin=sold.vin
    WHERE sold.id='{customer_id}'
    ORDER BY sold.saledate DESC, sold.vin ASC;
    """

    # sql for Gross Customer Income drill down - repairs
    SELECT_GROSS_INCOME_BY_CUSTOMER_REPAIR = """
    select distinct r.vin, r.startdate,COALESCE(r.completiondate::text, 'In Progress') AS completiondate,r.odometerreading,r.laborcharges,
    CASE
        WHEN temp.total_part_cost is null THEN 0
        ELSE temp.total_part_cost 
    END AS total_part_cost,
    concat(p.firstname,' ',p.lastname) serviceWriter,
    CASE
        WHEN temp.total_part_cost is null THEN r.laborcharges
        WHEN temp.total_part_cost is not null THEN r.laborcharges+temp.total_part_cost
    END as total_repair_cost from Repair r left join (select vin,sum(quantity*price) as total_part_cost from part group by vin)temp on r.vin=temp.vin
    inner join privilegeduser p on r.servicewriterusername=p.username
    where r.customerid='{customer_id}'
    ORDER BY r.startdate DESC,completiondate DESC,r.vin ASC;
    """

    #sql for Repair by manufacture report
    SELECT_REPAIR_MF = """
    select m.mfname manufacturer_name,count(r2.vin) total_number_repair,CASE
    WHEN sum(r2.laborcharges) is null THEN 0
    ELSE sum(r2.laborcharges)
    END AS total_labor_charges, CASE
        WHEN sum(r2.total_part_cost) is null THEN 0
        ELSE sum(r2.total_part_cost)
    END AS total_part_cost, CASE
        WHEN sum(r2.total_repair_cost) is null THEN 0
        ELSE sum(r2.total_repair_cost)
    END AS total_repair_cost from manufacturer m left join (select r.vin,v.mfname,r.laborcharges,temp.total_part_cost,CASE
        WHEN temp.total_part_cost is null THEN r.laborcharges
        WHEN temp.total_part_cost is not null THEN r.laborcharges+temp.total_part_cost
    END as total_repair_cost from Repair r left join (select vin,sum(quantity*price) as total_part_cost from part group by vin)temp on r.vin=temp.vin
    inner join vehicle v
    on r.vin=v.vin) r2 on r2.mfname=m.mfname
    GROUP BY m.mfname
    ORDER BY m.mfname ASC;
    """

    # sql for Repair by manufacture report - drill down
    SELECT_REPAIR_MF_TYPE = """
    select v.type,v.mname,count(distinct r.vin) total_number_repair,sum(r.laborcharges) total_labor_charges,sum(temp.total_part_cost) total_part_cost,CASE
    WHEN sum(temp.total_part_cost) is null THEN sum(r.laborcharges)
    WHEN sum(temp.total_part_cost) is not null THEN sum(r.laborcharges)+sum(temp.total_part_cost)
    END as total_repair_cost from Repair r left join (select vin,sum(quantity*price) as total_part_cost from part group by vin)temp on r.vin=temp.vin
    inner join vehicle v
    on r.vin=v.vin
    WHERE v.mfname='{manufacturer_name}'
    group by v.type,v.mname
    order by total_number_repair DESC;
    """
