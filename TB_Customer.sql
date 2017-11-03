CREATE TABLE TB_Customer(
    CustomerID int NOT NULL,
    Title varchar(255),
    FirstName varchar(255) NOT NULL,
    MiddleName varchar(255),
    LastName varchar(255) NOT NULL,
    Suffix varchar(255),
    EmailAddress varchar(255),
    Phone varchar(255),
    Gender varchar(255) NOT NULL,
    Birthdate date NOT NULL,
	CONSTRAINT PK_Customer PRIMARY KEY (CustomerID)
)
