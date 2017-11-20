SELECT f.ShipmentMethod, l.CountryRegion, 
    (COUNT(*) / (SELECT COUNT(*) 
        FROM DM_FactSales f1 JOIN DM_Location l1 ON f1.ShipToAddressID = l1.AddressID 
        WHERE l1.CountryRegion = l.CountryRegion) * 100) 
    AS 'Percentage of Late Shipment' 
FROM DM_FactSales f JOIN DM_Location l ON f.ShipToAddressID = l.AddressID
WHERE IsLateShipment != 0
GROUP BY f.ShipmentMethod, l.CountryRegion
ORDER BY l.CountryRegion, f.ShipmentMethod;
