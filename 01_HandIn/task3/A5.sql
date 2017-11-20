SELECT c.Name AS CustomerName, SUM(OrderLineProfit) AS Profit
FROM DM_FactSales f JOIN DM_Customer c ON f.CustomerID = c.CustomerID
WHERE YEAR(OrderDate) = 2014 AND MONTH(OrderDate) <= 6
GROUP BY c.Name
ORDER BY Profit DESC LIMIT 10;
