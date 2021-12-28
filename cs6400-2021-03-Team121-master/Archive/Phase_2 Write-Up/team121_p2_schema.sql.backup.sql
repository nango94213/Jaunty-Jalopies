CREATE TABLE PrivilegedUser (
	Username VARCHAR(30) NOT NULL,
	Password VARCHAR(20) NOT NULL,
	Firstname VARCHAR(30) NOT NULL,
	Lastname VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username)
);

CREATE TABLE ServiceWriter (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE Manager (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE Owner (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE SalesPerson (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE InventoryClerk (
	Username VARCHAR(30) NOT NULL,
	PRIMARY KEY (Username),
	CONSTRAINT fk_privilegeduser
		FOREIGN KEY (Username)
	    	REFERENCES PrivilegedUser (Username)
);

CREATE TABLE Manufacturer (
	MFName VARCHAR(50) NOT NULL,
	PRIMARY KEY (MFName)
);

CREATE TABLE Vehicle (
	VIN VARCHAR(17) NOT NULL,
	Description VARCHAR(200) NOT NULL,
	InvoicePrice FLOAT NOT NULL,
	Type VARCHAR(20) NOT NULL,
	Year SMALLINT NOT NULL,
	MName VARCHAR(30) NOT NULL,
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

CREATE TABLE Vehicle_Color (
	VIN VARCHAR(17) NOT NULL,
	Color VARCHAR(20) NOT NULL,
	PRIMARY KEY (VIN, Color),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);


CREATE TABLE SUV (
	VIN VARCHAR(17) NOT NULL,
	NumberOfCupHolders SMALLINT NOT NULL,
	DriveTrainType VARCHAR (30) NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE Van (
	VIN VARCHAR(17) NOT NULL,
	HasDriverSideBackDoor VARCHAR(1) NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);


CREATE TABLE Truck (
	VIN VARCHAR(17) NOT NULL,
	CargoCapacity VARCHAR(20) NOT NULL,
	CargoCoverType VARCHAR(20) NOT NULL,
	NoRearAxles VARCHAR(1) NOT Null,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);


CREATE TABLE Convertible (
	VIN VARCHAR(17) NOT NULL,
	BackSeatCount SMALLINT NOT NULL,
	RoofType VARCHAR(20) NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE Car (
	VIN VARCHAR(17) NOT NULL,
	NumberOfDoors SMALLINT NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN)
);

CREATE TABLE Individual (
	DriverLicenseNumber VARCHAR(30) NOT NULL,
	FirstName VARCHAR(30) NOT NULL,
	LastName VARCHAR(30) NOT NULL,
	Address VARCHAR(200) NOT NULL,
	PhoneNumber VARCHAR(15) NOT NULL,
	EmailAddress VARCHAR(50) NOT NULL,
	PRIMARY KEY (DriverLicenseNumber)
);


CREATE TABLE Vehicle_Sold_Individual (
	VIN VARCHAR(17) NOT NULL,
	DriverLicenseNumber VARCHAR(30) NOT NULL,
	SalesPersonUserName VARCHAR(30) NOT NULL,
	SaleDate DATE NOT NULL,
	SoldPrice FLOAT NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN),
	CONSTRAINT fk_DL
		FOREIGN KEY (DriverLicenseNumber)
	    	REFERENCES Individual (DriverLicenseNumber),
	CONSTRAINT fk_SalesUser
		FOREIGN KEY (SalesPersonUserName)
		REFERENCES SalesPerson (UserName)
);

CREATE TABLE Repair (
	VIN VARCHAR(17) NOT NULL,
	StartDate DATE NOT NULL,
	RDescription VARCHAR(500) NOT NULL,
	CompletionDate DATE NOT NULL,
	OdometerReading INTEGER NOT NULL,
	LaborCharges FLOAT NOT NULL,
	PRIMARY KEY (VIN)
);

CREATE TABLE Individual_Needs_Repair (
	DriverLicenseNumber VARCHAR(30) NOT NULL,
	VIN VARCHAR(17) NOT NULL,
	PRIMARY KEY (DriverLicenseNumber),
	CONSTRAINT fk_DL
		FOREIGN KEY (DriverLicenseNumber)
	    	REFERENCES Individual (DriverLicenseNumber),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Repair (VIN)
);


CREATE TABLE Business (
	TIN VARCHAR(30) NOT NULL,
	BName VARCHAR(100) NOT NULL,
	PCName VARCHAR(100) NOT NULL,
	Title VARCHAR(50) NOT NULL,
	Address VARCHAR(200) NOT NULL,
	PhoneNumber VARCHAR(15) NOT NULL,
	EmailAddress VARCHAR(50) NOT NULL,
	PRIMARY KEY (TIN)
);


CREATE TABLE Vehicle_Sold_Business (
	VIN VARCHAR(17) NOT NULL,
	TIN VARCHAR(30) NOT NULL,
	SalesPersonUserName VARCHAR(30) NOT NULL,
	SaleDate DATE NOT NULL,
	SoldPrice FLOAT NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Vehicle (VIN),
	CONSTRAINT fk_TIN
		FOREIGN KEY (TIN)
	    	REFERENCES Business(TIN),
	CONSTRAINT fk_SalesUser
		FOREIGN KEY (SalesPersonUserName)
		REFERENCES SalesPerson (UserName)
);

CREATE TABLE Business_Needs_Repair (
	TIN VARCHAR(30) NOT NULL,
	VIN VARCHAR(17) NOT NULL,
	PRIMARY KEY (TIN),
	CONSTRAINT fk_TIN
		FOREIGN KEY (TIN)
	    	REFERENCES Business (TIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Repair (VIN)
);


CREATE TABLE Part (
	VIN VARCHAR(17) NOT NULL,
	PartNumber VARCHAR(50) NOT NULL,
	VendorName VARCHAR(50) NOT NULL,
	Quantity SMALLINT NOT NULL,
	Price FLOAT NOT NULL,
	PRIMARY KEY (VIN),
	CONSTRAINT fk_vin
		FOREIGN KEY (VIN)
	    	REFERENCES Repair (VIN)
);

