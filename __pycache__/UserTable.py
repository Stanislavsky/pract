import tkinter as tk
from tkinter import ttk, messagebox
from InteractionWithTheDatabase import InteractionWithTheDatabase

class UserTable():
    def __init__(self, root):
        self.root = root
        self.frameTable = tk.Frame(root)
        self.frameTable.place(relx=0, rely=0.13, relheight=0.2, relwidth=1)
        self.columns = ("personID", "firstName", "secondName", "surname", "gender", "dateOfBirth")
        self.tree = ttk.Treeview(self.frameTable, columns=self.columns, show="headings")
        self.vsb = ttk.Scrollbar(self.frameTable, orient="vertical", command=self.tree.yview)
        
    def tableOutput(self):

        self.vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=1)

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        persons = interactionWithTheDatabase.weAskForEmployees()
        interactionWithTheDatabase.closeConnection()

        self.tree.heading("firstName", text="Имя")
        self.tree.heading("secondName", text="Фамилия")
        self.tree.heading("surname", text="Отчество")
        self.tree.heading("gender", text="Пол")
        self.tree.heading("dateOfBirth", text="День рождения")

        self.tree.column("firstName", width=100)
        self.tree.column("secondName", width=100)
        self.tree.column("surname", width=100)
        self.tree.column("gender", width=100)
        self.tree.column("dateOfBirth", width=100)

        self.tree.column("personID", width=0, stretch=tk.NO)
        self.tree.heading("personID", text="ID", anchor=tk.W)

        for person in persons:
            self.tree.insert("", tk.END, values=person)

    def giveId(self):
        selected_item = self.tree.selection()[0]
        self.person_id = self.tree.item(selected_item)['values'][0]
        return self.person_id
    
        