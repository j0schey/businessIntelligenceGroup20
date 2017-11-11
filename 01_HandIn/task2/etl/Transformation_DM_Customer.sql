INSERT INTO bi_olap_20.dm_customer (CustomerID, `Name`, BirthDate, Age, Gender, Email, Phone)
SELECT 
CustomerID,
concat(
FirstName,
	coalesce(
		concat(' [',MiddleName,'.]'),''),
	' ', LastName,
    coalesce(
        concat(' [',Suffix,']'),'')
        ),
BirthDate,
timestampdiff(year, BirthDate, '2016-01-01'),
substring(Gender, 1),
EmailAddress,
Phone
FROM bi_oltp_20.tb_customer