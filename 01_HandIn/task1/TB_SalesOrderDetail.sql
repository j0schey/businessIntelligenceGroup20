CREATE TABLE TB_SalesOrderDetail (
	SalesOrderID int NOT NULL,
    SalesOrderDetailID int NOT NULL,
    OrderQty int NOT NULL,
    ProductID int NOT NULL,
    UnitPrice decimal(15,5) NOT NULL,
    
    CONSTRAINT PK_SalesOrderDetail PRIMARY KEY (SalesOrderID, SalesOrderDetailID),
    CONSTRAINT FK_SalesOrder_SalesOrderDetail FOREIGN KEY (SalesOrderID) 
    REFERENCES TB_SalesOrderHeader(SalesOrderID),
    CONSTRAINT FK_Product_SalesOrderDetail FOREIGN KEY (ProductID)
    REFERENCES TB_Product(ProductID)
)