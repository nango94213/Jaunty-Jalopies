CREATE TABLE IF NOT EXISTS PrivilegedUser (
	Username VARCHAR(30) NOT NULL,
	Password VARCHAR(100) NOT NULL,
	Firstname VARCHAR(30) NOT NULL,
	Lastname VARCHAR(30) NOT NULL,
	Role VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username)
);

CREATE TABLE IF NOT EXISTS ServiceWriter (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE IF NOT EXISTS Manager (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE IF NOT EXISTS Owner (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE IF NOT EXISTS SalesPerson (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE IF NOT EXISTS InventoryClerk (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE IF NOT EXISTS Manufacturer (
	MFName VARCHAR(50) NOT NULL,
	PRIMARY KEY (MFName)
);

CREATE TABLE IF NOT EXISTS Vehicle (
	VIN VARCHAR(17) NOT NULL,
	Description VARCHAR(200),
	InvoicePrice FLOAT NOT NULL,
	Type VARCHAR(20) NOT NULL,
	Year SMALLINT NOT NULL,
	MName VARCHAR(50) NOT NULL,
	DateAdded DATE NOT NULL,
	IClerkUserName VARCHAR(30) NOT NULL,
	MFName VARCHAR(50) NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_iclerkusername
		FOREIGN KEY (IClerkUserName)
	    	REFERENCES InventoryClerk (Username),
	CONSTRAINT fk_mfname
		FOREIGN KEY (MFName)
	    	REFERENCES Manufacturer (MFName)
);

CREATE TABLE IF NOT EXISTS Vehicle_Color (
	VIN VARCHAR(17) NOT NULL,
	Color VARCHAR(20) NOT NULL,
	PRIMARY KEY (VIN, Color),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE IF NOT EXISTS SUV (
	VIN VARCHAR(17) NOT NULL,
	NumberOfCupHolders SMALLINT NOT NULL,
	DriveTrainType VARCHAR (30) NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE IF NOT EXISTS Van (
	VIN VARCHAR(17) NOT NULL,
	HasDriverSideBackDoor BOOL NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE IF NOT EXISTS Truck (
	VIN VARCHAR(17) NOT NULL,
	CargoCapacity VARCHAR(20) NOT NULL,
	CargoCoverType VARCHAR(40),
	NoRearAxles VARCHAR(1) NOT Null,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE IF NOT EXISTS Convertible (
	VIN VARCHAR(17) NOT NULL,
	BackSeatCount SMALLINT NOT NULL,
	RoofType VARCHAR(30) NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE IF NOT EXISTS Car (
	VIN VARCHAR(17) NOT NULL,
	NumberOfDoors SMALLINT NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE IF NOT EXISTS Customer (
	ID VARCHAR(30) NOT NULL,
	Address VARCHAR(200) NOT NULL,
	PhoneNumber VARCHAR(20) NOT NULL,
	EmailAddress VARCHAR(50),
	PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Individual (
	DriverLicenseNumber VARCHAR(30) NOT NULL,
	FirstName VARCHAR(30) NOT NULL,
	LastName VARCHAR(30) NOT NULL,
	PRIMARY KEY (DriverLicenseNumber),
	CONSTRAINT fk_id
		FOREIGN KEY (DriverLicenseNumber)
	    	REFERENCES Customer (ID)
);

CREATE TABLE IF NOT EXISTS Business (
	TIN VARCHAR(30) NOT NULL,
	BName VARCHAR(100) NOT NULL,
	PCName VARCHAR(100) NOT NULL,
	Title VARCHAR(50) NOT NULL,
	PRIMARY KEY (TIN),
	CONSTRAINT fk_id
		FOREIGN KEY (TIN)
	    	REFERENCES Customer (ID)
);

CREATE TABLE IF NOT EXISTS Vehicle_Sold_Customer (
	VIN VARCHAR(17) NOT NULL,
	ID VARCHAR(30) NOT NULL,
	SalesPersonUserName VARCHAR(30) NOT NULL,
	SaleDate DATE NOT NULL,
	SoldPrice FLOAT NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN),
	CONSTRAINT fk_ID
		FOREIGN KEY (ID)
	    	REFERENCES Customer (ID),
	CONSTRAINT fk_SalesUser
		FOREIGN KEY (SalesPersonUserName)
		REFERENCES SalesPerson (UserName)
);

CREATE TABLE IF NOT EXISTS Repair (
	VIN VARCHAR(17) NOT NULL,
	CustomerID VARCHAR(30) NOT NULL,
	StartDate DATE NOT NULL,
	ServiceWriterUsername VARCHAR(30) NOT NULL,
	RDescription VARCHAR(500) NOT NULL,
	CompletionDate DATE,
	OdometerReading INTEGER NOT NULL,
	LaborCharges FLOAT,
	PRIMARY KEY (VIN, CustomerID, StartDate),
	CONSTRAINT fk_ID
		FOREIGN KEY (CustomerID)
	    	REFERENCES Customer (ID),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN),
	CONSTRAINT fk_service_writer
		FOREIGN KEY (ServiceWriterUsername)
	    	REFERENCES ServiceWriter (Username)
);

CREATE TABLE IF NOT EXISTS Part (
	VIN VARCHAR(17) NOT NULL,
	CustomerID VARCHAR(30) NOT NULL,
	StartDate DATE NOT NULL,
	PartNumber VARCHAR(50) NOT NULL,
	VendorName VARCHAR(50) NOT NULL,
	Quantity SMALLINT NOT NULL,
	Price FLOAT NOT NULL,
	-- PRIMARY KEY (VIN, CustomerID, StartDate),
	CONSTRAINT fk_repair_key
		FOREIGN KEY (VIN, CustomerID, StartDate)
	    	REFERENCES Repair (VIN, CustomerID, StartDate)
);
