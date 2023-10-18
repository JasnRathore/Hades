from prettytable import PrettyTable
from datetime import *
from CRONUS import *

def guards_salary(Cursor):
    Cursor.execute("SELECT sum(SALARY) from guards;")
    salary = (Cursor.fetchone())[0]
    if salary == None:
        salary = 0
    Cursor.execute(f"UPDATE expenditure SET rate = {salary} where EXPENSES = 'Guards'")

def view_rates(Cursor,mode = "income"):
    if mode == "income":
        mytable = PrettyTable(["Cell_Block","Rate"])
        Cursor.execute("SELECT * FROM Income;")
        for row in Cursor:
            lst=[]
            for data in row:
                lst.append(str(data))
            mytable.add_row(lst)
        print()
        return (mytable)
    elif mode == "expenditure":
        guards_salary(Cursor)
        mytable = PrettyTable(["Expenses","Rate"])
        Cursor.execute("SELECT * FROM Expenditure;")
        for row in Cursor:
            lst=[]
            for data in row:
                lst.append(str(data))
            mytable.add_row(lst)
        print()
        return (mytable)

def view_fund(Cursor):
    #Fetches rates of Incomes
    Cursor.execute("SELECT sum(rate) from Income natural join Prisoners;")
    Income = Cursor.fetchone()[0]
    if Income == None:
        Income = 0
    #Fetches rates of expenditure
    guards_salary(Cursor)
    Cursor.execute("SELECT sum(Rate) FROM Expenditure")
    
    Expenditure = (Cursor.fetchone())[0]
    #Fetches Balance
    Cursor.execute("SELECT Amount FROM Balance")
    Balance = (Cursor.fetchone())[0]
    print(f"\nIncome [Daily]:{Income}, Income [Monthly]: {Income*30}")
    print(f"Expenditure [Daily]: {Expenditure}, Expendiutre [Monthly]: {Expenditure*30}")
    print(f"Revenue [Daily]: {Income-Expenditure}, Revenue [Monthly]: {(Income-Expenditure)*30}")
    print(f"Balance: {Balance}")

def view_transactions(Cursor):
    mytable = PrettyTable(["No.","Date","Time","[                Description                ]","Amount"])
    Cursor.execute("SELECT * FROM Transaction;")
    for row in Cursor:
        lst=[]
        for data in row:
            lst.append(str(data))
        mytable.add_row(lst)
    print(mytable)

def modify(Cursor,mode = "income"):
    if mode == "income":
        print(view_rates(Cursor,mode="income"))
        while True:
            SelectedCellBlock = input("Please select Cell_Block Rate to be modified: ").upper()
            if SelectedCellBlock in ["A","B","C"]:
                new_rate = int(input("Enter new rate: "))
                Cursor.execute(f"UPDATE INCOME SET RATE = {new_rate} where CELL_BLOCK = '{SelectedCellBlock}';")
                print("Update Successful!")
                print(view_rates(Cursor,mode="income"))
                break
            else:
                print("Please select a valid cellblock!")
    if mode == "expenditure":
        print(view_rates(Cursor,mode="expenditure"))
        while True:
            SelectedUtility = input("Expense Rate to be modified: ").upper()
            if SelectedUtility in ['MAINTANENCE','WATER','ELECTRICITY','FOOD','HEALTHCARE']:
                new_rate = int(input("Enter new rate: "))
                Cursor.execute(f"UPDATE EXPENDITURE SET RATE = {new_rate} where EXPENSES = '{SelectedUtility}';")
                print("Update Successful!")
                print(view_rates(Cursor,mode="expenditure"))
                break
            elif SelectedUtility in ["GUARDS"]:
                print("You do not have permission to edit guards salary [Chief Guard User Required!]")
            else:
                print("Please select a valid expense!")

def funds(Cursor,mode = "add"):
    Cursor.execute("SELECT COUNT(*) FROM Transaction")
    transaction_no = Cursor.fetchone()[0] + 1
    date_now = str(datetime.today())
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M:%S")
    while True:
        description = input("Describe Transaction [50 char max]: ")
        if len(description) < 50:
            break
        else:
            print("Description exceeded 50 characters! Please enter again!")
    while True:
        funds = int(input("Please enter amount: "))
        if funds > 100000000:
            print("Transaction limit is 10 crores!")
        else:
            break
    if mode == "add":
        pass
    if mode == "deduct":
        funds = -funds
    Cursor.execute(f"Update Balance Set amount = amount + {funds};")
    Cursor.execute("Select * from Balance;")
    Balance = (Cursor.fetchone())[0]
    print(f"Balance: {Balance}")
    Cursor.execute(f"INSERT INTO TRANSACTION VALUES('{transaction_no}','{date_now}','{current_time}','{description}','{funds}');")

def finance_menu(DataBase, Cursor):
    while True:
        print(f"""\n-------------------------------------HERMES-------------------------------------\n
1) View Transaction History
2) View Income, Expenditure, Revenue & Balance
3) Modify Income
4) Modify Expenditure
5) Add Funds
6) Deduct Funds
7) Exit
"""
)
        try:
            menu_chc = int(input("Please select a choice [1/2/3/4/5/6/7]: "))
        except:
            print("Invalid Input!")
            continue
        if menu_chc==1:
            view_transactions(Cursor)
        elif menu_chc==2:
            view_fund(Cursor)
        elif menu_chc==3:
            modify(Cursor,mode="income")
        elif menu_chc==4:
            modify(Cursor,mode="expenditure")
        elif menu_chc==5:
            funds(Cursor,mode="add")
        elif menu_chc == 6:
            funds(Cursor,mode="deduct")
        elif menu_chc==7:
            break
        else:
            print("Invalid input! ")
        DataBase.commit()
