CREATE TABLE DM_Product(
ProductID int NOT NULL,
ProductNumber varchar(200),
`Name` varchar(200),
ModelName varchar (200),
StandardCost decimal(15,2),
ListPrice decimal(15,2),
ProductSubCategory int,
ProductTopCategory int,
SellStartDate date NOT NULL,
SellEndDate date,
DiscontinuedDate date,
Size varchar(20),
Weight decimal(15,2),
IsBulkyItem int,
CONSTRAINT PK_Product PRIMARY KEY (ProductID),
CONSTRAINT FK_SellStartDate_Product FOREIGN KEY (SellStartDate)
	REFERENCES DM_Time(`Date`),
CONSTRAINT FK_SellEndDate_Product FOREIGN KEY (SellEndDate)
	REFERENCES DM_Time(`Date`),
CONSTRAINT FK_DiscontinuedDate_Product FOREIGN KEY (DiscontinuedDate)
	REFERENCES DM_Time(`Date`)
)