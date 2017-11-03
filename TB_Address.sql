CREATE TABLE TB_Address (
	AddressID int NOT NULL,
    AddressLine varchar(255) NOT NULL,
    City varchar(255) NOT NULL,
    StateProvince varchar(255),
    PostalCode varchar(255) NOT NULL,
    CountryRegion varchar(255) NOT NULL,
	CONSTRAINT PK_Address PRIMARY KEY (AddressID)
)
