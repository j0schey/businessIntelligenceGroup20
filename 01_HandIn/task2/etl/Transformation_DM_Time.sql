CREATE PROCEDURE p_time(IN startdate DATE,IN stopdate DATE)
BEGIN
DECLARE currentdate DATE;
SET currentdate = startdate;
WHILE currentdate < stopdate DO
    INSERT INTO dm_time VALUES (
    currentdate,
    DAY(currentdate),
    MONTH(currentdate),
	YEAR(currentdate));
SET currentdate = DATE_ADD(currentdate,INTERVAL 1 DAY);
END WHILE;
END