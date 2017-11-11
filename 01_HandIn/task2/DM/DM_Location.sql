CREATE TABLE DM_Location(
AddressID int NOT NULL,
PostalCode varchar(10),
City varchar(100),
StateProvince varchar(100),
CountryRegion varchar(100),
CONSTRAINT PK_Location PRIMARY KEY (AddressID)
)