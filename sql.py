import sqlite3

# Connect to SQLite
connection = sqlite3.connect("employee.db")

# Create a cursor object to insert, create, and retrieve
cursor = connection.cursor()

# Creating table
table_info = """
CREATE TABLE EMPLOYEE (
    NAME VARCHAR(30),
    DEPARTMENT VARCHAR(30),
    EMPLOYEE_ID VARCHAR(30),
    SALARY INT
);
"""

cursor.execute(table_info)

# Inserting some records
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Pranjal','Data Science','12001',100000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Aditya','Product','12002',80000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Bhoumik','ML','12003',120000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Abhinav','AI','12004',100000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Shresth','Data Science','12005',85000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Ankit','Product','12006',95000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Chimyang','Product','12007',97500)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Somnath','ML','12008',86500)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES ('Ashwini','SDE','12009',100000)''')

# Display all records
print("The inserted records are")

data = cursor.execute('''SELECT * FROM EMPLOYEE''')

for row in data:
    print(row)

# Committing and closing the connection
connection.commit()
connection.close()
