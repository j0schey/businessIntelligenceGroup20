SELECT MONTH(OrderDate) AS Month, SUM(TaxAmount) as TaxAmount
FROM DM_FactSales
WHERE YEAR(OrderDate) = 2014 AND MONTH(OrderDate) <= 7
GROUP BY Month
ORDER BY Month;
