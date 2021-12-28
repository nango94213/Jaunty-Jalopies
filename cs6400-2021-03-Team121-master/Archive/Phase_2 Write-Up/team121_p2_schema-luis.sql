CREATE TABLE PrivilegedUser (
	username VARCHAR(80) NOT NULL,
	password VARCHAR(50) NOT NULL,
	firstname VARCHAR(50) NOT NULL,
	lastname VARCHAR(50) NOT NULL,
	PRIMARY KEY (username)
);

CREATE TABLE ServiceWriter (
	username VARCHAR(80) NOT NULL,
	PRIMARY KEY (username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (username)
	    	REFERENCES PrivilegedUser (username)
);

CREATE TABLE Manager (
	username VARCHAR(80) NOT NULL,
	PRIMARY KEY (username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (username)
	    	REFERENCES PrivilegedUser (username)
);

CREATE TABLE Owner (
	username VARCHAR(80) NOT NULL,
	PRIMARY KEY (username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (username)
	    	REFERENCES PrivilegedUser (username)
);

CREATE TABLE SalesPerson (
	username VARCHAR(80) NOT NULL,
	PRIMARY KEY (username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (username)
	    	REFERENCES PrivilegedUser (username)
);

CREATE TABLE InventoryClerk (
	username VARCHAR(80) NOT NULL,
	PRIMARY KEY (username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (username)
	    	REFERENCES PrivilegedUser (username)
);

CREATE TABLE Manufacturer (
	name VARCHAR(80) NOT NULL,
	PRIMARY KEY (name)
);

CREATE TABLE Vehicle (
	vin VARCHAR(17) NOT NULL,
	description VARCHAR(100) NOT NULL,
	invoice_price FLOAT NOT NULL,
	type VARCHAR(50) NOT NULL,
	year SMALLINT NOT NULL,
	model_name VARCHAR(50) NOT NULL,
	date_added DATE NOT NULL,
	inventory_clerk_username VARCHAR(80) NOT NULL,
	manufacturer_name VARCHAR(80) NOT NULL,
	PRIMARY KEY (vin),
	CONSTRAINT fk_iclerkusername
		FOREIGN KEY (inventory_clerk_username)
	    	REFERENCES InventoryClerk (username),
	CONSTRAINT fk_mfname
		FOREIGN KEY (manufacturer_name)
	    	REFERENCES Manufacturer (name)
);