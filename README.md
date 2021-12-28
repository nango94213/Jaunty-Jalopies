# cs6400-2021-03-Team121

## Requirements
You will have to have docker installed in your computer to start up application.  

## Technologies used
- Python
- Flask
- Postgres (PSQL)
- Docker  

## SQL statements
Most SQL statements, queries and/or transactions for this project can be found in folder [sql_](sql_).  

## How to run
1. Open project folder using terminal.
2. Execute: `docker-compose up --build`  
3. Open a browser and go into: 
    1. localhost:8001
    2. 127.0.0.1:8001  

## Demo Data
By default, biggest data set from demo_data is added. If smaller set of demo data wanted, then uncomment `SOURCE_DATA: 'demo_data'` line in [docker-compose.yml](docker-compose.yml).

## DB Persistence
For data persistence on this project, after executing `docker-compose up --build` a file **dbs** will be created on the inmediate up level from the directory where command was executed.

## HOW TOs
### Access DB
On a separate terminal, you can run: `docker exec -it jaunty_jalopies_db bash -c "psql postgres postgres"`  

### Not to populate DB at container start and persist data
Go into [docker-compose.yml](docker-compose.yml) and uncomment line with environment variable `RESET_DB`. Then stand up your containers with `docker-compose up`.  

### Persist new data if volume was previously created
If you see `PostgreSQL Database directory appears to contain a database; Skipping initialization` when trying to recreate a new volume,  
execute this command: `docker-compose down --volumes` and `docker-compose up --build` afterwards.

### See SQL transactions sent to DB
Go into [docker-compose.yml](docker-compose.yml) and uncomment line `command: postgres -c log_statement=all`.  

### Avoid SQL Injection in Python
There is information about it here: [https://www.psycopg.org/docs/sql.html#module-usage](https://www.psycopg.org/docs/sql.html#module-usage).  
Try login in with this user: `johnDoe'; DROP TABLE ServiceWriter; SELECT PrivilegedUser WHERE username='peter`

## General Info
VIN Numbers were gotten from here: [https://vingenerator.org/brand](https://vingenerator.org/brand)  

### Owner Role
For the owner role to be able to take any role, at the time of creating an owner it is necessary to add her/him to all existing user tables.  

### Changes to Schema
Design is a constant process, you change your design while you code and test. During phase3 we changed schema from phase2 of project and the new schema 
is located in [sql_/team121_p3_schema.sql](sql_/team121_p3_schema.sql). To see changes, do a diff against 
[archive/Phase_2/team121_p2_schema.sql](archive/Phase_2/team121_p2_schema.sql).  
The relation for the previous schema is located on: [archive/Phase_2/team121_p2_eer2rel.pdf](archive/Phase_2/team121_p2_eer2rel.pdf), while the relation for the new schema is located on: [docs/team121_p3_updatedEerRel.pdf](docs/team121_p3_updatedEerRel.pdf).  

### Some sample data to insert
| Vehicle Type             | SUV               | Convertible           | Car               | Van                       | Truck                   |
| ------------------------ |:------------------| :-------------------- | :---------------- | :------------------------ | :---------------------- |
| VIN Number               | WA19FAFL8DA202124 | 1GCFG15X471203088     | JT2AL22G0C4449167 | WDBSK7BA6BF161906         | 1N6BA0CC0AN303535       |
| Description              | 2021 Audi Q7      | 2021 Chevrolet Camaro | 2022 Toyota Camry | 2022 Mercedes Benz Metris | 2021 Nissan Titan XD    |
| Invoice Price            | 54950             | 25000                 | 25295             | 33920                     | 45430                   |
| Model Name               | Q7                | Camaro                | Camry             | Metris                    | Titan XD                |
| Model Year               | 2021              | 2021                  | 2022              | 2022                      | 2021                    |
| Manufacturer             | Audi              | Chevrolet             | Toyota            | Mercedes Benz             | Nissan                  |
| Color(s)                 | Blue              | White,Black           | Grey              | Black                     | Red                     |
| # Cupholders             | 6                 |                       |                   |                           |                         |
| Drivetrain Type          | FWD               |                       |                   |                           |                         |
| Back Seat Count          |                   | 2                     |                   |                           |                         |
| Roof Type                |                   | detachable hardtop    |                   |                           |                         |
| # Doors                  |                   |                       | 4                 |                           |                         |
| Has Driver Side Backdoor |                   |                       |                   | No                        |                         |
| Cargo Capacity           |                   |                       |                   |                           | 2400                    |
| Cargo Cover Type         |                   |                       |                   |                           | high impact plastic lid |
| # Rear Axles             |                   |                       |                   |                           | 2                       |

| Customer Type            | Individual         | Business              |
| ------------------------ |:-------------------| :-------------------- |
| ID                       | JD93-647-829-102-9 | 123-45-678            |
| Address                  | 2021 Example Rd.   | 2021 Georgia Tech St. |
| Phone Number             | +1(813)763-9808    | +1(305)987-1023       |
| Email Address            | jdoe2021@gmail.com | stevej@example1.com   |
| Firstname                | John               |                       |
| Lastname                 | Doe                |                       |
| Business Name            |                    | Example One           |
| Primary Contact Name     |                    | Steve Jovs            |
| Primary Contact Title    |                    | Employee 0            |


### Small Dataset
| Username | Type             |  Password      |
| :------- | :--------------- | :------------- |
| ding     | Service Writer   | staycurious    |
| om       | Manager          | beproductive   |
| yinan    | Sales Person     | simplyawesome  |
| leo      | Sales Person     | markthisday    |
| rolan    | Owner            | imtheceo       |
| luis     | Inventory Clerk  | wh4t3v3r       |

# Big Dataset
| Username | Type             |  Password      |
| :------- | :--------------- | :------------- |
| roland   | Owner            | roland         |
| user01   | Sales Person     | pass01         |
| user02   | Manager          | pass02         |
| user03   | Inventory Clerk  | pass03         |
| user12   | Service Writer   | pass12         |


## Authors
* __Ding Yuan__  email: [dyuan47@gatech.edu](mailto:dyuan47@gatech.edu)
* __Om Sachdev__  email: [osachdev3@gatech.edu](mailto:osachdev3@gatech.edu)
* __Yinan Yang__  email: [yyang601@gatech.edu](mailto:yyang601@gatech.edu)
* __Luis Humberto Orozco Cabrera__  email: [lcabrera32@gatech.edu](lcabrera32@gatech.edu)