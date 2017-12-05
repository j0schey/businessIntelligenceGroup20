CREATE TABLE TB_CustomerAddress (
	CustomerID int NOT NULL,
    AddressID int NOT NULL,
    AddressType varchar(255) NOT NULL,
	CONSTRAINT PK_CustomerAddress PRIMARY KEY (CustomerID, AddressID),
    CONSTRAINT FK_Customer_CustomerAddress FOREIGN KEY (CustomerID)
    REFERENCES TB_Customer(CustomerID),
	CONSTRAINT FK_Address_CustomerAddress FOREIGN KEY (AddressID)
    REFERENCES TB_Address(AddressID)
)