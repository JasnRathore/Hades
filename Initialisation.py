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
    Cursor.execute("CREATE TABLE GUARDS (GNO int(3) PRIMARY KEY,NAME VARCHAR(25),AGE INT,GENDER CHAR(1),SALARY INT,CELL_BLOCK CHAR(1),DUTY_START_TIME TIME,DUTY_END_TIME TIME);")
    Cursor.execute("CREATE TABLE Contraband (ITEMID int(3) PRIMARY KEY,ITEMNAME VARCHAR(25),QUANTITY INT);")
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
