## Requirements
You will have to have docker installed in your computer to start up application.  

## Technologies used
- Python
- Flask
- Postgres (PSQL)
- Docker  

## SQL statements
All SQL statements, queries and/or transactions for this project can be found in folder [sql_](sql_).  

## How to run
1. Open project folder using terminal.
2. Execute: `docker-compose up --build`  
3. Open a browser and go into: 
    1. localhost:8001
    2. 127.0.0.1:8001  

## HOW TOs
### Access DB
On a separate terminal, you can run: `docker exec -it jaunty_jalopies_db bash -c "psql postgres postgres"`  

### Not to populate DB at container start and persist data
Go into [docker-compose.yml](docker-compose.yml) and uncomment line with environment variable `RESET_DB`. Then stand up your containers with `docker-compose up`.  

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

## Authors
* __Om Sachdev__  email: [osachdev3@gatech.edu](mailto:osachdev3@gatech.edu)
* __Yinan Yang__  email: [yyang601@gatech.edu](mailto:yyang601@gatech.edu)
* __Luis Humberto Orozco Cabrera__  email: [lcabrera32@gatech.edu](lcabrera32@gatech.edu)
