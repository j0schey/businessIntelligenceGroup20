SELECT ProductTopCategory, SUM(OrderLineTotal) AS Revenue
FROM DM_FactSales f JOIN DM_Product p on f.ProductID = p.ProductID
WHERE YEAR(OrderDate) = 2014
GROUP BY ProductTopCategory
ORDER BY ProductTopCategory;
