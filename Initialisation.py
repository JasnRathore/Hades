import mysql.connector
import random

def init():
    DataBaseName = 'hades'
    try:
        DataBase = mysql.connector.connect(host="localhost", user="root", password="root")
        print("Connection to SQL Successful.")
    except mysql.connector.Error as err:
        print("Error:", err)
        return None, None, False
    #Connection Successful
    Cursor = DataBase.cursor()
    Cursor.execute("SHOW DATABASES;")
    DataBases = []               
    for DB in Cursor.fetchall():
        DataBases.append(DB[0])
    if DataBaseName in DataBases:
        print(f"Connected to Database: {DataBaseName}")
        Cursor.execute(f"USE {DataBaseName};")
        return Cursor, DataBase, True
    #Database Not Found
    print("Database Not Detected\nCreating Database")
    Cursor.execute(f"CREATE DATABASE {DataBaseName};")
    Cursor.execute(f"USE {DataBaseName};")
    Cursor.execute("CREATE TABLE Prisoners (PNO int(3) PRIMARY KEY,NAME VARCHAR(25),AGE INT,GENDER CHAR(1),CRIME VARCHAR(50),SENTENCE INT,CELL_BLOCK CHAR(1),PAROLE INT(1),RELEASE_DATE DATE);")
    Cursor.execute("CREATE TABLE Guards (GNO int(3) PRIMARY KEY,NAME VARCHAR(25),AGE INT,GENDER CHAR(1),SALARY INT,CELL_BLOCK CHAR(1),DUTY_START_TIME TIME,DUTY_END_TIME TIME);")
    Cursor.execute("CREATE TABLE Login (USER varchar(25), PASSW varchar(25));")
    Cursor.execute("INSERT INTO Login(USER,PASSW) VALUES('WARDEN',1234),('CHIEF_OFFICER',1234),('FINANCE_OFFICER',1234);")
    Cursor.execute("CREATE TABLE Transaction (NO int,DATE date,TIME varchar(10),DESCRIPTION varchar(50),AMOUNT int(10));")
    Cursor.execute("CREATE TABLE Income (CELL_BLOCK varchar(10),RATE int(10));")
    Cursor.execute("INSERT INTO Income VALUES('A',500),('B',700),('C',1000);")
    Cursor.execute("CREATE TABLE Expenditure (EXPENSES varchar(100),RATE int(10));")
    Cursor.execute("INSERT INTO Expenditure(EXPENSES,RATE) VALUES('MAINTANENCE',5000),('WATER',2000),('ELECTRICITY',500),('FOOD',500),('HEALTHCARE',1000),('GUARDS',0);")
    Cursor.execute("Create TABLE Balance(AMOUNT int(20));")
    Cursor.execute("Insert INTO Balance(AMOUNT) values(10000);")
    print("Tables Created")
    return Cursor, DataBase, True

#generating primary key values when required in table    
def random_no(Cursor,Table):
    r=random.randint(10000,99999)
    Cursor.execute(f"SELECT * FROM {Table};")
    for i in Cursor:
        if i[0]==r:
            random_no(Cursor,Table)
    return r
