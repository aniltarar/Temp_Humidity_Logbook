BEGIN TRANSACTION;

CREATE TABLE LogbookTemp(
	ID INTEGER PROMARY KEY,
	DATE TEXT,
	TIME TEXT,
	'Temperature C' FLOAT,
	Humidity FLOAT
);

INSERT INTO LogbookTemp(ID,DATE,Time,'Temperature C',Humidity)
SELECT ID, Date, Time, Temperature, humidity
FROM Logbook;

DROP TABLE Logbook;

ALTER TABLE LogbookTemp
RENAME TO Logbook;

COMMIT;