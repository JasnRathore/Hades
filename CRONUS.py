import random
from prettytable import PrettyTable
from Initialisation import *

def DateValidate(Date): #Only Valid for(YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD)
    try:
        if len(Date) == 10 and Date[4] in '-/':
            return 1 <= int(Date[5:7]) <= 12 and 1 <= int(Date[8:]) <= 31
        elif len(Date) == 8:
            return 1 <= int(Date[4:6]) <= 12 and 1 <= int(Date[6:]) <= 31
    except ValueError:
        pass
    return False
        
def GetValidInput(prompt, valid_options):
    while True:
        user_input = input(prompt).upper()
        if user_input in valid_options:
            return user_input
        print("Invalid INPUT\n")

def InputPrisonerData(Cursor, mode = "A"):
    if mode == 'A':
        PNO = random_no(Cursor, "prisoners")
    elif mode == 'M':
        Cursor.execute(f"SELECT PNO FROM prisoners;")
        PrisonersNos = [prisoner[0] for prisoner in Cursor.fetchall()]
        while True:
            PNO = int(input("Enter PNO to Modify:"))
            if PNO in PrisonersNos:
                break
            print ("PNO dosent exist\n")

    Cursor.execute(f"SELECT NAME FROM prisoners;")
    Names = []                                      #Happy
    for Name in Cursor.fetchall():
        Names.append(Name[0])
    while True:
        Name = input("Please enter name: ")
        if Name not in Names:
            break
        print("Records with inputted name exist!")
        if GetValidInput("Do you wish to continue [Y/N]: ",("Y", "N")) == "Y":
            break

    while True:
        Age = input("Please enter age: ")
        if Age.isdigit() or (mode == 'M' and Age ==""):
            if Age.isdigit():
                Age = int(Age)
            break
        print("invalid Age\n")

    while True:
        Gender = input("Please enter gender [M/F]: ").upper()
        if Gender in ("M", "F") or (mode == "M" and Gender == ""):
            break
        print("Invalid gender. Please enter 'M' or 'F'.")

    while True:
        Crime = input("Enter Crime: ")
        if Crime != "" or (Crime == "" and mode == "M"):
            break
        print("Invalid Input\n")

    while True:
        Sentence = input("Please enter Sentence: ")
        if Sentence.isdigit() or (mode == 'M' and Sentence ==""):
            if Sentence.isdigit():
                Sentence = int(Sentence)
            break
        print("invalid Sentence\n")

    while True:
        CellBlock = input("Please enter cell block [A/B/C]: ").upper()
        if CellBlock in ("A", "B", "C")  or (mode == "M" and CellBlock ==""):
            break
        print("Invalid cell block. Please enter 'A', 'B', or 'C'.")
    print("Parole [Yes/No]\n1) NO\n2) YES\n")
    while True:
        Parole = (input("Enter Option no:"))
        if  Parole.isdigit() :
            Parole = int(Parole)
            if Parole in (1,2):
                Parole -= 1
                break
        elif mode == "M" and Parole == "":
            break
        print("\ninvalid Option\n")
    while True:
        ReleaseDate = input("Enter Release Date(YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD):")
        if DateValidate(ReleaseDate) is True or (mode == "M" and ReleaseDate == ""):
            break
        print("\nInvalid Date\n")    
    return PNO, Name, Age, Gender, Crime, Sentence, CellBlock, Parole, ReleaseDate

def AddPrisoner(DataBase, Cursor):
    while True:
        print("Add record")
        data = InputPrisonerData(Cursor, "A")
        Cursor.execute("INSERT INTO prisoners VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);", data)
        DataBase.commit()
        print("\nRecord added\n")
        if GetValidInput("Do you wish to add another record? [Y/N]: ", ("Y", "N")) == "N":
            break

def ModifyPrisoner(DataBase, Cursor):
    while True:
        print("Modify record")
        Data = list(InputPrisonerData(Cursor, "M"))
        Cursor.execute(f"SELECT * FROM Prisoners WHERE PNO = {Data[0]};")
        PreviousData = Cursor.fetchone()
        for i in range(len(Data)):
            if Data[i] =="":
                Data[i] = PreviousData[i]
        Name = Data.pop(0)
        Data.append(Name)
        Cursor.execute("UPDATE prisoners SET NAME = %s, AGE = %s, GENDER = %s, CRIME = %s, SENTENCE = %s, CELL_BLOCK = %s, PAROLE = %s, RELEASE_DATE = %s WHERE PNO = %s;", tuple(Data))
        DataBase.commit()
        print("\nRecord Updated\n")
        if GetValidInput("Do you wish to Update another record? [Y/N]: ", ("Y", "N")) == "N":
            break

def DeletePrisoner(DataBase, Cursor):
    while True:
        Cursor.execute("SELECT PNO FROM prisoners;")
        PrisonersNos = [prisoner[0] for prisoner in Cursor.fetchall()]
        PNO = int(input("Enter PNO to DELETE:"))
        if PNO not in PrisonersNos:
            print ("PNO dosent exist\n")
            break
        Cursor.execute(f"DELETE FROM prisoners WHERE PNO = {PNO}")
        DataBase.commit()
        print("\nRecord Deleted\n")
        if GetValidInput("Do you wish to Update another record? [Y/N]: ", ("Y", "N")) == "N":
            break

def PrisonerView(Cursor):
    Cursor.execute("SELECT * FROM prisoners;")
    mytable = PrettyTable(["PNO","Name","Age","Gen","Crime", "Sentence","Cell","Parole","RD"])
    for row in Cursor.fetchall():
        mytable.add_row(list(row))
    print(mytable)

def PrisonerMenu(DataBase, Cursor):
    Options = {1: PrisonerView, 2: AddPrisoner, 3: ModifyPrisoner, 4: DeletePrisoner}
    while True:
        print('''
1) View Prisoner Details
2) Add Prisoner Details
3) Modify Prisoner Details
4) Delete Prisoner Details
5) Exit
''')
        MenuOpt = int(input("Please select a choice [1/2/3/4/5]: "))
        if MenuOpt==1:
            Options[MenuOpt](Cursor)
        elif MenuOpt==5:
            break
        elif MenuOpt in Options:
            Options[MenuOpt](DataBase, Cursor)
        else:
            print("Invalid input! ")