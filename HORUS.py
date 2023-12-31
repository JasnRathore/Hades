from prettytable import PrettyTable
from Initialisation import *

def TimeValidate(Time): #Only valid for(HH:MM:SS,HHMMSS)
    try:
        if len(Time)== 8 and Time[2] in ':':
            return 0 <= int(Time[0:2]) <=24 and 0 <= int(Time[3:5]) <= 59 and 0 <= int(Time[6:]) <= 59
        elif len(Time)==6:
            return 0 <= int(Time[0:2]) <=24 and 0 <= int(Time[2:4]) <= 59 and 0 <= int(Time[4:]) <= 59
    except ValueError:
        pass
    return False

def InputGuards(Cursor,mode):
    if mode=='A':
        GNO = random_no(Cursor,"guards")
    elif mode=='M':
        #Checking if GNO exists
        Cursor.execute(f"SELECT GNO FROM guards;")
        ListOfGuardNos=[]
        for Guard in Cursor.fetchall():
            ListOfGuardNos.append(Guard[0])
        while True:
            GNO = int(input("Enter GNO to Modify:"))
            if GNO in ListOfGuardNos:
                break
            print ("GNO dosent exist\n")
    Cursor.execute(f"SELECT NAME FROM guards;")
    ListOfNames = []
    for Row in Cursor.fetchall():
        ListOfNames.append(Row[0])
    while True:
        Name = input("Please enter name: ")
        if (Name == "" and mode == "A"):
            print("Cant leave Input field empty")
        elif (Name == "" and mode == "M") or (Name not in ListOfNames):
            break
        else:
            print("Records with inputted name exist!")
            check_chc = (input("Do you wish to continue [Y/N]: ")).upper()
            print()
            if check_chc == "Y":
                break
    while True:
        age=input("Please enter an age: ")
        #Checking for valid age
        if age.isdigit() and int(age)>18:
            age=int(age)
            break
        elif mode=='M' and age == "":
            break
        else:
            print("Please enter a valid age!")
    while True:
        gender = input("Please enter gender [M/F]: ").upper()
        #Checking for valid gender
        if (gender == "F" or gender == "M"):
            break
        elif mode=='M'and gender == "":
            break
        else:
            print("Please select  valid gender!")
    while True:
        salary = input("Please enter salary: ")
        #Checking for valid salary
        if salary.isdigit():
            salary=int(salary)
            break
        elif mode=='M' and salary == "":
            break
        else:
            print("Please enter a valid salary!")
    while True:
        cb = input("Please enter cell block [A/B/C]: ").upper()
        #Checking for valid cellblock
        if cb in ("A", "B", "C"):
            break
        elif mode=='M' and cb=="":
            break
        else:
            print("Please select valid cell block!\n")
    while True:
        dst=input("Please enter duty start time (HH:MM:SS,HHMMSS):")
        if TimeValidate(dst) is True or (mode == "M" and dst == ""):
            break
        print("\nInvalid time\n")
    while True:
        det=input("Please enter duty end time (HH:MM:SS,HHMMSS):")
        if TimeValidate(det) is True or (mode == "M" and det == ""):
            break
        print("\nInvalid time\n")

    return GNO,Name,age,gender,salary,cb,dst,det

def view(Cursor):
    Cursor.execute(f"SELECT * FROM guards;")
    mytable = PrettyTable(["GNO","Name","Age","Gen","Salary","Cell","StartTime","EndTime"])
    for row in Cursor:
        lst=[]
        for data in row:
            lst.append(str(data))
        mytable.add_row(lst)
    print(mytable)

def add(DataBase,Cursor):
    while True:
        print("--------------------------------Add Record--------------------------------")
        fields=InputGuards(Cursor,'A')
        Cursor.execute("INSERT INTO guards VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",fields)
        DataBase.commit()
        print("\nRecord added\n")
        add_chc = input("Do you wish to add another record? [Y/N]: ").upper()
        if add_chc == "Y":
            continue
        else:
            break

def modify(DataBase,Cursor):
    while True:
        view(Cursor)
        print("--------------------------------Modify Record--------------------------------")
        fields=list(InputGuards(Cursor,'M'))
        Cursor.execute(f"SELECT * FROM guards WHERE GNO={fields[0]};")
        PreviousData=Cursor.fetchone()
        for i in range(len(fields)):
            if fields[i]=="":
                fields[i]=PreviousData[i]
        GNO=fields.pop(0)
        fields.append(GNO)
        update = f"UPDATE guards SET NAME = %s,AGE = %s,GENDER = %s,SALARY = %s,CELL_BLOCK = %s,DUTY_START_TIME = %s,DUTY_END_TIME = %s WHERE GNO = %s;"
        Cursor.execute(update,fields)
        DataBase.commit()
        print("\nRecord updated\n")
        modify_chc = input("Do you wish to modify another record? [Y/N]: ").upper()
        if modify_chc == "Y":
            continue
        else:
            break
def search(Cursor):
    print("--------------------------------Search Record--------------------------------")
    GNO = input("Enter GNO to search: ")
    #Checking for valid gno
    if GNO.isdigit()==False:
        print("Invalid input!")
        return
    Cursor.execute(f"SELECT * FROM guards WHERE GNO = {GNO};")
    result = Cursor.fetchall()
    if len(result)==0:
        print("No records found for the given GNO.")
    else:
        mytable = PrettyTable(["GNO", "Name", "Age", "Gen", "Salary", "Cell", "StartTime", "EndTime"])
        for row in result:
            mytable.add_row(list(row))
        print(mytable)

def delete(DataBase,Cursor):
    while True:
        view(Cursor)
        print("--------------------------------Delete Record--------------------------------")
        GNO=input("Enter the guard number of the record to be deleted: ")
        #Checking for valid gno
        if GNO.isdigit()==False:
            print("Invalid input!")
            return
        #Checking if GNO exists
        Cursor.execute(f"SELECT * FROM guards WHERE GNO = {GNO};")
        result = Cursor.fetchall()
        if len(result)==0:
            print("No records found for the given GNO.")
        else:
            delete=f"DELETE FROM guards WHERE GNO={GNO}"
            Cursor.execute(delete)
            DataBase.commit()
            print("\nRecord deleted\n")
            del_chc = input("Do you wish to delete another record? [Y/N]: ").upper()
            if del_chc == "Y":
                continue
            else:
                break

def guards_menu(DataBase,Cursor):
    while True:
        print('''
--------------------------------Menu--------------------------------
1) View Guard Details
2) Add Guard Details
3) Modify Guard Details
4) Search Guard Details
5) Delete Guard Details
6) Exit''')
        try:
            menu_chc = int(input("Please select a choice [1/2/3/4/5]: "))
        except:
            print("Invalid Input!")
            continue
        if menu_chc==1:
            view(Cursor)
        elif menu_chc==2:
            add(DataBase,Cursor)
        elif menu_chc==3:
            modify(DataBase,Cursor)
        elif menu_chc==4:
            search(Cursor)
        elif menu_chc==5:
            delete(DataBase,Cursor)
        elif menu_chc==6:
            break
        else:
            print("Invalid input! ")
