from Initialisation import *
from HORUS import *
from CRONUS import *

def main():
    Cursor, DataBase, Connected = init()
    if Connected is True:
        #we can do menu(Cursor, DataBase) or menu(DataBase) and we define the cursor in the funtion
        menu(Cursor, "guards")
        DataBase.commit()

main()

