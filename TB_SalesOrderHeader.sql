CREATE TABLE TB_SalesOrderHeader (
	SalesOrderID int NOT NULL,
    RevisionNumber int NOT NULL,
    OrderDate date NOT NULL,
    DueDate date NOT NULL,
    ShipDate date,
    Status varchar(255) NOT NULL,
    SalesOrderNumber varchar(255) NOT NULL,
    CustomerID int NOT NULL,
    ShipToAddressID int NOT NULL,
    BillToAddressID int NOT NULL,
    ShipMethodID int NOT NULL,
    CONSTRAINT PK_SalesOrderHeader PRIMARY KEY (SalesOrderID),
    CONSTRAINT FK_Customer_SalesOrderHeader FOREIGN KEY (CustomerID)
    REFERENCES TB_Customer(CustomerID),
	CONSTRAINT FK_ShipToAddress_SalesOrderHeader FOREIGN KEY (ShipToAddressID)
    REFERENCES TB_Address(AddressID), 
    CONSTRAINT FK_BillToAddress_SalesOrderHeader FOREIGN KEY (BillToAddressID)
    REFERENCES TB_Address(AddressID),
    CONSTRAINT FK_ShipMethod_SalesOrderHeader FOREIGN KEY (ShipMethodID)
    REFERENCES TB_ShipMethod(ShipMethodID)
)