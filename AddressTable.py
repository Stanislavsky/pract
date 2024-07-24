import tkinter as tk
from tkinter import ttk, messagebox
from InteractionWithTheDatabase import InteractionWithTheDatabase

class AdressTable():
    def __init__(self, root, userTable):
        self.root = root
        self.frameTable = tk.Frame(root)
        self.userTable = userTable
        self.frameTable.place(relx=0, rely=0.67, relheight=0.2, relwidth=1)
        self.columns = ("addressID", "city", "street", "apartmentNumber", "personID","typeOfAdressID")
        self.tree = ttk.Treeview(self.frameTable, columns=self.columns, show="headings")
        self.vsb = ttk.Scrollbar(self.frameTable, orient="vertical", command=self.tree.yview)
        
    def tableOutput(self, event=None):
        
        self.clearTable()
        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        person_id = self.userTable.giveId() 

        if person_id is None:
            return

        address = interactionWithTheDatabase.addressOutput(person_id)
        
        interactionWithTheDatabase.closeConnection()
        
        self.vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=1)

        self.tree.heading("typeOfAdressID", text="Тип адреса")
        self.tree.heading("city", text="Город")
        self.tree.heading("street", text="Улица")
        self.tree.heading("apartmentNumber", text="Номер квартиры")

        self.tree.column("typeOfAdressID", width=100)
        self.tree.column("city", width=100)
        self.tree.column("street", width=100)
        self.tree.column("apartmentNumber", width=100)

        self.tree.column("personID", width=0, stretch=tk.NO)
        self.tree.heading("personID", text="ID", anchor=tk.W) 
        self.tree.column("addressID", width=0, stretch=tk.NO)
        self.tree.heading("addressID", text="ID", anchor=tk.W) 

        for addres in address: 
            self.tree.insert("", tk.END, values=addres)
    
    def clearTable(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def giveId(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return None
           
        else:
            selected_item = selected_items[0]
            self.adressId = self.tree.item(selected_item)['values'][0]
            return self.adressId
