CREATE TABLE TB_ShipMethod (
	ShipMethodID int NOT NULL,
	Name varchar(255) NOT NULL,
	CostPerShipment decimal(15,5) NOT NULL,
	CostPerUnit decimal(15,5) NOT NULL,
    BulkyItemSurcharge decimal (10,5) NOT NULL,
    CONSTRAINT PK_ShipMethod PRIMARY KEY (ShipMethodID)
)