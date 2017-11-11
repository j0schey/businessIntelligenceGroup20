INSERT INTO bi_olap_20.dm_product(ProductID, ProductNumber, `Name`, ModelName, StandardCost, ListPrice, ProductSubCategory, ProductTopCategory, SellStartDate, SellEndDate, DiscontinuedDate, Size, Weight, IsBulkyItem)
SELECT `tb_product`.`ProductID`,
    `tb_product`.`ProductNumber`,
    `tb_product`.`Name`,
	`tb_product`.`ProductModelName`,
    `tb_product`.`StandardCost`,
    `tb_product`.`ListPrice`,

    `tb_product`.`ProductCategoryID`,
        -- ProductTopCategory:  
	tb_productcategory.ParentProductCategoryID,
    `tb_product`.`SellStartDate`,
    `tb_product`.`SellEndDate`,
    `tb_product`.`DiscontinuedDate`,
    `tb_product`.`Size`,
    `tb_product`.`Weight`,
	-- IsBulkyItem:
    CASE
		WHEN tb_productcategory.ParentProductCategoryID  = 1 THEN 1
		WHEN tb_productcategory.ProductCategoryID IN (16, 18, 20) THEN 1
		ELSE 0
	END
    as BulkyItem
FROM bi_oltp_20.tb_product inner join bi_oltp_20.tb_productcategory ON 
		bi_oltp_20.tb_product.ProductCategoryID = bi_oltp_20.tb_productcategory.ProductCategoryID
