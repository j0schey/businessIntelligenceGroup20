INSERT INTO bi_olap_20.dm_location (AddressID, PostalCode, City, StateProvince, CountryRegion)
SELECT 
AddressID, PostalCode, City, StateProvince, CountryRegion
FROM bi_oltp_20.tb_address