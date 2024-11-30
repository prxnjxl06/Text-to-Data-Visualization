-- Create Worker table

DROP TABLE IF EXISTS Worker;
CREATE TABLE Worker (
	WORKER_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	FIRST_NAME TEXT,
	LAST_NAME TEXT,
	SALARY INTEGER,
	JOINING_DATE TEXT,
	DEPARTMENT TEXT
);

-- Insert values into Worker table
INSERT INTO Worker 
	(WORKER_ID, FIRST_NAME, LAST_NAME, SALARY, JOINING_DATE, DEPARTMENT) VALUES
		(1, 'Monika', 'Arora', 100000, '2020-02-14 09:00:00', 'HR'),
		(2, 'Niharika', 'Verma', 80000, '2011-06-14 09:00:00', 'Admin'),
		(3, 'Vishal', 'Singhal', 300000, '2020-02-14 09:00:00', 'HR'),
		(4, 'Amitabh', 'Singh', 500000, '2020-02-14 09:00:00', 'Admin'),
		(5, 'Vivek', 'Bhati', 500000, '2011-06-14 09:00:00', 'Admin'),
		(6, 'Vipul', 'Diwan', 200000, '2011-06-14 09:00:00', 'Account'),
		(7, 'Satish', 'Kumar', 75000, '2020-01-14 09:00:00', 'Account'),
		(8, 'Geetika', 'Chauhan', 90000, '2011-04-14 09:00:00', 'Admin');

-- Create Bonus table
DROP TABLE IF EXISTS Bonus;
CREATE TABLE Bonus (
	WORKER_REF_ID INTEGER,
	BONUS_AMOUNT INTEGER,
	BONUS_DATE TEXT,
	FOREIGN KEY (WORKER_REF_ID) REFERENCES Worker(WORKER_ID) ON DELETE CASCADE
);

-- Insert values into Bonus table
INSERT INTO Bonus 
	(WORKER_REF_ID, BONUS_AMOUNT, BONUS_DATE) VALUES
		(1, 5000, '2016-02-20'),
		(2, 3000, '2016-06-11'),
		(3, 4000, '2016-02-20'),
		(1, 4500, '2016-02-20'),
		(2, 3500, '2016-06-11');

-- Create Title table
DROP TABLE IF EXISTS Title;
CREATE TABLE Title (
	WORKER_REF_ID INTEGER,
	WORKER_TITLE TEXT,
	AFFECTED_FROM TEXT,
	FOREIGN KEY (WORKER_REF_ID) REFERENCES Worker(WORKER_ID) ON DELETE CASCADE
);

-- Insert values into Title table
INSERT INTO Title 
	(WORKER_REF_ID, WORKER_TITLE, AFFECTED_FROM) VALUES
		(1, 'Manager', '2016-02-20 00:00:00'),
		(2, 'Executive', '2016-06-11 00:00:00'),
		(8, 'Executive', '2016-06-11 00:00:00'),
		(5, 'Manager', '2016-06-11 00:00:00'),
		(4, 'Asst. Manager', '2016-06-11 00:00:00'),
		(7, 'Executive', '2016-06-11 00:00:00'),
		(6, 'Lead', '2016-06-11 00:00:00'),
		(3, 'Lead', '2016-06-11 00:00:00');
