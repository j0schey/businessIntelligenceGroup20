CREATE TABLE DM_Customer(
CustomerID int NOT NULL,
`Name` varchar(150),
BirthDate date,
Age int,
Gender varchar(10),
Email varchar(255),
Phone varchar(255),
CONSTRAINT PK_Customer PRIMARY KEY (CustomerID)
)