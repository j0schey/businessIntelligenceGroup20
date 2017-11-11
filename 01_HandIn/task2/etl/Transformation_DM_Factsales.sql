-- Inserting keys & columns without transformation
INSERT INTO bi_olap_20.dm_factsales(SalesOrderNumber, SalesOrderLineNumber, CustomerID, ProductID, ShipToAddressID, BillToAddressID, ShipmentMethod, UnitPrice, orderDate, dueDate, shipDate, OrderQuantity, orderStatus)
SELECT
tb_salesorderheader.SalesOrderNumber,
CONCAT ('SOL', tb_salesorderdetail.SalesOrderID,'-',SalesOrderDetailID) AS SalesOrderLineNumber,
tb_salesorderheader.CustomerID,
tb_salesorderdetail.ProductID,
tb_salesorderheader.ShipToAddressID,
tb_salesorderheader.BillToAddressID,
tb_shipmethod.name AS ShipmentMethod,
tb_salesorderdetail.unitPrice,
tb_salesorderheader.orderDate,
tb_salesorderheader.dueDate,
tb_salesorderheader.shipDate,
tb_salesorderdetail.orderQty,
tb_salesorderheader.status

FROM ((bi_oltp_20.tb_salesorderdetail INNER JOIN bi_oltp_20.tb_salesorderheader 
 ON bi_oltp_20.tb_salesorderdetail.SalesOrderID = bi_oltp_20.tb_salesorderheader.SalesOrderID)
 INNER JOIN bi_oltp_20.tb_shipmethod ON bi_oltp_20.tb_salesorderheader.ShipMethodID = bi_oltp_20.tb_shipmethod.ShipMethodID);

-- Updating Discount
UPDATE
dm_factsales
INNER JOIN dm_product ON dm_factsales.productID = dm_product.productID
SET dm_factsales.Discount =
dm_factsales.orderQuantity * dm_factsales.unitPrice * 
CASE
	WHEN dm_product.ProductTopCategory = 1 THEN null
	WHEN dm_product.ProductTopCategory = 2 THEN null
	WHEN dm_product.ProductTopCategory = 3 AND dm_factsales.OrderQuantity BETWEEN 5 AND 9 THEN 0.05
    WHEN dm_product.ProductTopCategory = 3 AND dm_factsales.OrderQuantity >= 10 THEN 0.1
    WHEN dm_product.ProductTopCategory = 4 AND dm_factsales.OrderQuantity BETWEEN 5 AND 9 THEN 0.04
    WHEN dm_product.ProductTopCategory = 4 AND dm_factsales.OrderQuantity >= 10 THEN 0.11
END;

-- Updating OrderLineTotal & OrderLineProfit
UPDATE 
dm_factsales
INNER JOIN dm_product ON dm_factsales.productID = dm_product.productID
SET

OrderLineTotal = 
(OrderQuantity * UnitPrice - IFNULL(Discount, 0)),
OrderLineProfit = 
(OrderLineTotal - OrderQuantity * StandardCost);

-- Updating TaxAmount
UPDATE
dm_factsales
INNER JOIN dm_location ON dm_factsales.ShipToAddressID = dm_location.AddressID
SET taxAmount = 
OrderLineTotal * 
CASE
	WHEN dm_location.CountryRegion LIKE "United States" THEN 0.08
    WHEN dm_location.CountryRegion LIKE "Canada" THEN 0.13
    WHEN dm_location.CountryRegion LIKE "United Kingdom" THEN 0.175
    WHEN dm_location.CountryRegion LIKE "Australia" THEN 0.10
END;

-- Updating Freight Cost
UPDATE 
(dm_factsales
INNER JOIN helptable_freightcost ON dm_factsales.ShipmentMethod = helptable_freightcost.ShipmentMethod)
INNER JOIN dm_product ON dm_factsales.productID = dm_product.productID
SET OrderLineFreightCost =
(OrderQuantity * perItemCost) + IF(dm_product.IsBulkyItem = 1, bulkyItemSurcharge, 0);

-- Updating IsLateShipment
UPDATE
dm_factsales
SET IsLateShipment = 
IF(ShipDate > DueDate, 1, 0)
