CREATE TABLE helpTable_FreightCost(
ShipmentMethod varchar(100),
perShipmentCost int,
perItemCost int,
bulkyItemSurcharge int);
INSERT INTO helpTable_FreightCost
VALUES
('Standard Ground', 5, 2, 8),
('Cargo International', 8, 5, 10),
('Oversea Deluxe', 32, 7, 12);


