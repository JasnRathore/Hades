from datetime import datetime,time
import random
from prettytable import PrettyTable
from Initialisation import *

def chk_time(time):
    time_format="%H:%M:%S"
    #Checking if format matches the time
    try:
        datetime.strptime(time,time_format)
    except ValueError:
        return False
    
def str_to_time(time_str):
    #Converting string to time
    time_format="%H:%M:%S"
    time=datetime.strptime(time_str,time_format).time()
    return time
    
def view(Cursor):
    Cursor.execute(f"SELECT * FROM guards;")
    mytable = PrettyTable(["GNO","Name","Age","Gen","Salary","Cell","StartTime","EndTime"])
    for row in Cursor:
        lst=[]
        for data in row:
            lst.append(str(data))
        mytable.add_row(lst)

    print(mytable)
        
def add(Cursor):
    while True:
        print("--------------------------------Add Record--------------------------------")
        gno=random_no(Cursor,"guards")
        name = input("Please enter name: ")
        #Checking for name repetition
        
        Cursor.execute(f"SELECT * FROM guards;")
        result = Cursor.fetchall()
        for i in result:
            if i[1] == name:
                print("Records with inputted name exist!")
                check_chc = (input("Do you wish to continue [Y/N]: ")).upper()
                print()
                if check_chc == "Y":
                    pass
                else:
                    break
            
        age = int(input("Please enter age: "))

        gender = input("Please enter gender [M/F]: ").upper()
        #Checking for valid gender
        if gender != "F" and gender != "M":
            print("Please select  valid gender!\n")
            break

        salary=int(input("Please enter salary: "))
        
        cb = input("Please enter cell block [A/B/C]: ").upper()
        #Checking for valid cellblock
        if cb not in ("A", "B", "C"):
            print("Please select  valid cell block!\n")
            break
            
        dst=input("Please enter duty start time[hh:mm:ss]: ")
        if chk_time(dst)==False:
            print("Invalid time string ")
            break

        det=input("Please enter duty end time[hh:mm:ss]: ")
        if chk_time(det)==False:
            print("Invalid time string ")
            break
            
        data=[gno,name,age,gender,salary,cb,dst,det]
        insert=(f"INSERT INTO guards values (%s,%s,%s,%s,%s,%s,%s,%s)")
        Cursor.execute(insert,data)
        print("\nRecord added\n")
        add_chc = input("Do you wish to add another record? [Y/N]: ").upper()
        if add_chc == "Y":
            continue
        else:
            break
  
def modify(Cursor):
    while True:
        view(Cursor)
        print("--------------------------------Modify Record--------------------------------")
        gno=int(input("Enter the guard number of the record to be modified: "))
        #Checking if gno exists
        Cursor.execute("SELECT * from guards")
        result = Cursor.fetchall()
        for i in result:
            if i[0] == gno:
                guard_info = list(i)
                del guard_info[0]
                break
        else:
            print("Gno not found!")
            break
        print("Press Enter if you do not wish to modify field!\n")
        name = input("Please enter name: ")
        age = input("Please enter an age: ")
        if age.isdigit() or age == "":
            pass
        else:
            print("Please enter a valid age!")
            break

        gender = input("Please enter gender [M/F]: ").upper()

        #Checking for Valid Gender
        if (gender == "F" or gender == "M"):
            pass
        elif gender == "":
            pass
        else:
            print("Please select  valid gender!")
            break
            
        salary=input("Please enter salary: ")
        if age.isdigit() or age == "":
            pass
        else:
            print("Please enter a valid salary!")
            break
        cb = input("Please enter cell block [A/B/C]: ").upper()
        
        #Checking for valid cellblock
        if cb not in ("A","B","C","") :
            print("Please select  valid cell block!\n")
            break
            
        dst_str=input("Please enter duty start time[hh:mm:ss]: ")
        if chk_time(dst_str)==True:
            dst_str=str_to_time(dst_str)
        elif dst_str == "":
            pass
        else:
            print("Invalid time string!")
            break

        det_str=input("Please enter duty end time[hh:mm:ss]: ")
        if chk_time(det_str)==True:
            det_str=str_to_time(det_str)
        elif det_str == "":
            pass
        else:
            print("Invalid time string!")

        data=[name,age,gender,salary,cb,dst_str,det_str,gno]
        for i in range(len(data)):
            if data[i] == "":
                data[i] = guard_info[i]

        update = f"UPDATE guards SET NAME = %s,AGE = %s,GENDER = %s,SALARY = %s,CELL_BLOCK = %s,DUTY_START_TIME = %s,DUTY_END_TIME = %s WHERE gno = %s;"
        Cursor.execute(update,data)
        print("\nRecord updated\n")
        
        modify_chc = input("Do you wish to modify another record? [Y/N]: ").upper()
        if modify_chc == "Y":
            continue
        else:
            break

def delete(Cursor):
    while True: 
        view(Cursor)
        print("--------------------------------Delete Record--------------------------------")
        gno=int(input("Enter the guard number of the record to be deleted: "))
         #Checking if gno exists
        Cursor.execute("SELECT * from guards")
        result = Cursor.fetchall()
        for i in result:
            if int(i[0]) == gno:
                break
        else:
            print("Gno not found!")
            break
        delete=f"DELETE FROM guards WHERE GNO={gno}"
        Cursor.execute(delete)
        print("\nRecord deleted\n")
        del_chc = input("Do you wish to delete another record? [Y/N]: ").upper()
        if del_chc == "Y":
            continue
        else:
            break

def menu(Cursor,Guards):
    while True:
        print('''
--------------------------------Menu--------------------------------
1) View Guard Details
2) Add Guard Details
3) Modify Guard Details
4) Delete Guard Details
5) Exit
''')
        menu_chc = int(input("Please select a choice [1/2/3/4/5]: "))
        database = Guards
        if menu_chc==1:
            view(Cursor)
        elif menu_chc==2:
            add(Cursor)
        elif menu_chc==3:
            modify(Cursor)
        elif menu_chc==4:
            delete(Cursor)
        elif menu_chc==5:
            break
        else:
            print("Invalid input! ")
            break
    
    
