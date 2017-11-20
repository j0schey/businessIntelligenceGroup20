SELECT CountryRegion, SUM(OrderLineProfit) AS Profit
FROM DM_FactSales f JOIN DM_Location l ON f.BillToAddressID = l.AddressID
WHERE YEAR(OrderDate) = 2013
GROUP BY CountryRegion
ORDER BY Profit DESC;
