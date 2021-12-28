
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
    
    INSERT_SERVICE_WRITER = """INSERT INTO ServiceWriter 
                               VALUES ('{username}')"""
    
    INSERT_MANAGER = """INSERT INTO Manager 
                        VALUES ('{username}')"""
    
    INSERT_OWNER = """INSERT INTO Owner 
                      VALUES ('{username}')"""
    
    INSERT_SALES_PERSON = """INSERT INTO SalesPerson 
                             VALUES ('{username}')"""
    
    INSERT_INVENTORY_CLERK = """INSERT INTO InventoryClerk 
                                VALUES ('{username}')"""
    
    INSERT_OWNER = """INSERT INTO Owner 
                      VALUES ('{username}');
                      INSERT INTO ServiceWriter
                      VALUES ('{username}');
                      INSERT INTO Manager
                      VALUES ('{username}');
                      INSERT INTO SalesPerson
                      VALUES ('{username}');
                      INSERT INTO InventoryClerk
                      VALUES ('{username}');"""

    INSERT_MANUFACTURER = """INSERT INTO Manufacturer 
                             VALUES ('{name}')"""

    SELECT_USER = """SELECT * FROM PrivilegedUser
                     WHERE username = %s;"""

    SELECT_COUNT_CARS_AVAILABLE_FOR_SALE = """SELECT COUNT(vin) FROM Vehicle
                                              WHERE vin NOT IN (
                                                  SELECT vin FROM Vehicle_Sold_Customer
                                              );"""