CREATE TABLE DM_FactSales(
SalesOrderNumber varchar(100) NOT NULL,
SalesOrderLineNumber varchar(100) NOT NULL,
CustomerID int,
ProductID int,
ShipToAddressID int,
BillToAddressID int,
ShipmentMethod varchar(100),
UnitPrice decimal (15,5),
Discount numeric(10,4),
OrderQuantity int,
OrderLineTotal numeric(10,4),
OrderLineProfit numeric(10,4),
TaxAmount numeric(10,4),
OrderLineFreightCost numeric(10,4),
OrderStatus varchar(30),
OrderDate date,
DueDate date,
ShipDate date,
IsLateShipment int,

CONSTRAINT PK_FactSales PRIMARY KEY (SalesOrderNumber, SalesOrderLineNumber),
CONSTRAINT FK_CustomerID_FactSales FOREIGN KEY (CustomerID)
	REFERENCES DM_Customer(CustomerID),
CONSTRAINT FK_ProductID_FactSales FOREIGN KEY (ProductID)
	REFERENCES DM_Product(ProductID),
CONSTRAINT FK_ShipToAddressID_FactSales FOREIGN KEY (ShipToAddressID)
	REFERENCES DM_Location(AddressID),
CONSTRAINT FK_BillToAddressID_FactSales FOREIGN KEY (BillToAddressID)
	REFERENCES DM_Location(AddressID),
CONSTRAINT FK_OrderDate_FactSales FOREIGN KEY (OrderDate)
	REFERENCES DM_Time(`Date`),
CONSTRAINT FK_DueDate_FactSales FOREIGN KEY (DueDate)
	REFERENCES DM_Time(`Date`),
CONSTRAINT FK_ShipDate_FactSales FOREIGN KEY (ShipDate)
	REFERENCES DM_Time(`Date`)
)