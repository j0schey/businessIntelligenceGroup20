CREATE TABLE TB_ProductCategory(
	ProductCategoryID int NOT NULL,
    ParentProductCategoryID int,
    Name varchar(255) NOT NULL,
    CONSTRAINT PK_ProductCategory PRIMARY KEY (ProductCategoryID),
    CONSTRAINT FK_ParentProductCategory_ProductCategory FOREIGN KEY (ParentProductCategoryID)
    REFERENCES TB_ProductCategory(ProductCategoryID)
)