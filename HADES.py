from Initialisation import *
from HORUS import *
from CRONUS import *
from HERMES import *
import random

def main():
    Cursor, DataBase, Connected = init()
    if Connected is True:
        Cursor.execute("SELECT * FROM Login;")
        #User and Password details
        Data = Cursor.fetchall()
        Users,Passw=[],[]
        for rec in Data:
            Users.append(rec[0])
            Passw.append(rec[1])
        while True:
            print("""\n-----------------------------HADES-----------------------------------\n
1) Login
2) Change Password
3) Exit\n""")
            chc = int(input("Select a choice [1/2/3]: "))
            #Entering User
            if chc == 1:
                print("\n-----------------------------LOGIN-----------------------------\n")
                username = input("Enter Username: ").upper()
                if username not in Users:
                    print("Please enter valid username!")
                    print(f"Valid Users: {Users}")
                else:
                    Userno = Users.index(username)
                    password = input("Enter passsword [Case Sensitive]: ")
                    if password != Passw[Userno]:
                        print("Invalid Password! Try Again!")
                    else:
                        Access = {"WARDEN": PrisonerMenu, "CHIEF_OFFICER": guards_menu,"FINANCE_OFFICER": finance_menu}
                        Access[username](DataBase, Cursor)
                        break
            if chc == 2:
                while True:
                    print("\n-----------------------------CHANGE PASSWORD-----------------------------\n")
                    username = input("Enter Username: ").upper()
                    if username not in Users:
                        print("Please enter valid username!")
                        print(f"Valid Users: {Users}")
                        break
                    else:
                        Userno = Users.index(username)
                        password = input("Enter passsword [Case Sensitive]: ")
                        if password != Passw[Userno]:
                            print("Invalid Password! Try Again!")
                        else:
                            new_password = ""
                            for i in range(15):
                                new_password = new_password + chr(random.randrange(42,122))
                            print(new_password)
                            Cursor.execute(f"UPDATE LOGIN SET PASSW = '{new_password}' where User = '{Users[Userno]}';")
                            print("Password Updated!")
                            break
            if chc == 3:
                break
        DataBase.commit()

main()
