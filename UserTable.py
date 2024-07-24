import tkinter as tk
from tkinter import ttk, messagebox
from InteractionWithTheDatabase import InteractionWithTheDatabase
from CustomButton import CustomButton

class UserTable():
    
    def __init__(self, root):
        self.root = root
        self.frameTable = tk.Frame(root)
        self.frameTable.place(relx=0, rely=0.13, relheight=0.2, relwidth=1)
        self.columns = ("personID", "firstName", "secondName", "surname", "gender", "dateOfBirth")
        self.tree = ttk.Treeview(self.frameTable, columns=self.columns, show="headings")
        self.vsb = ttk.Scrollbar(self.frameTable, orient="vertical", command=self.tree.yview)
        
    def tableOutput(self):

        self.clearTable()
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

    def tableOutputError(self,selected_itemFullName):
        self.clearTable()
        self.vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=1)
        persons = selected_itemFullName
        
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

        for person in persons[0]:
            self.tree.insert("", tk.END, values=person)
        

    def tableOutputError2(self, selected_itemFullName):
        self.clearTable()
        self.vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=1)

        personsId = []
        for i in selected_itemFullName[0]:
            sub_sub_type = i[0]
            personsId.append(sub_sub_type)
        
        persons = []
        for item in selected_itemFullName[1]:
            sub_sub_itemType = item[1]
            if sub_sub_itemType in personsId:
                persons.append(sub_sub_itemType)
            if not personsId:
                persons.append(sub_sub_itemType)
            
        

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        necessaryPersons = interactionWithTheDatabase.weAskForEmployeesNecessary(persons)
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

        for person in necessaryPersons:
            self.tree.insert("", tk.END, values=person)

    def tableOutputError3(self, selected_itemFullName):
        self.clearTable()
        self.vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=1)
        
        personsId = []
        for i in selected_itemFullName[1]:
            sub_sub_type = i[1]
            personsId.append(sub_sub_type)

        for i in selected_itemFullName[0]:
            sub_sub_type = i[0]
            personsId.append(sub_sub_type)

        persons = []
        for i in selected_itemFullName[2]:
            sub_sub_itemType = i[4]
            if sub_sub_itemType in personsId:
                persons.append(sub_sub_itemType)
            if not personsId:
                persons.append(sub_sub_itemType)
            
        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        necessaryPersons = interactionWithTheDatabase.weAskForEmployeesNecessary(persons)
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

        for person in necessaryPersons:
            self.tree.insert("", tk.END, values=person)

    def giveId(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return None
           
        else:
            selected_item = selected_items[0]
            self.person_id = self.tree.item(selected_item)['values'][0]
            return self.person_id
    
    def clearTable(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        