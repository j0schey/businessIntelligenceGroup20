CREATE TABLE TB_Product (
	ProductID int NOT NULL,
    Name varchar(255) NOT NULL,
    ProductNumber varchar(255) NOT NULL,
    StandardCost decimal(15,5) NOT NULL,
    ListPrice decimal(15,5) NOT NULL,
    Size varchar(255),
    Weight decimal(15,5),
    ProductCategoryID int NOT NULL,
    ProductModelName varchar(255),
    SellStartDate date NOT NULL,
    SellEndDate date,
    DiscontinuedDate date,
    CONSTRAINT PK_Product PRIMARY KEY (ProductID),
    CONSTRAINT FK_ProductCategory_Product FOREIGN KEY (ProductCategoryID)
    REFERENCES TB_ProductCategory(ProductCategoryID)
)