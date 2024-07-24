import tkinter as tk
from tkinter import ttk, messagebox
from InteractionWithTheDatabase import InteractionWithTheDatabase
from UserTable import UserTable

class DocumentsTable():

    def __init__(self, root, userTable):
        self.root = root
        self.frameTable = tk.Frame(root)
        self.userTable = userTable
        self.frameTable.place(relx=0, rely=0.40, relheight=0.2, relwidth=1)
        self.columns = ( "passportDataID", "personID", "documentationReferenceID", "serialNumber", "numberPD", "dateOfIssue", "issuedByWhom")
        self.tree = ttk.Treeview(self.frameTable, columns=self.columns, show="headings")
        self.vsb = ttk.Scrollbar(self.frameTable, orient="vertical", command=self.tree.yview)
        self.person_id = None
        self.documentId = None
    
    def tableOutput(self, event=None):
        self.clearTable()
        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        person_id = self.userTable.giveId() 

        if person_id is None:
            return
        
        documents = interactionWithTheDatabase.documentOutput(person_id)
        interactionWithTheDatabase.closeConnection()

        self.vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=1)

        self.tree.heading("documentationReferenceID", text="Тип документа")
        self.tree.heading("serialNumber", text="Серия")
        self.tree.heading("numberPD", text="Номер")
        self.tree.heading("dateOfIssue", text="Дата получения")
        self.tree.heading("issuedByWhom", text="Кем выдан")

        self.tree.column("documentationReferenceID", width=100)
        self.tree.column("serialNumber", width=100)
        self.tree.column("numberPD", width=100)
        self.tree.column("dateOfIssue", width=100)
        self.tree.column("issuedByWhom", width=190)

        self.tree.column("personID", width=0, stretch=tk.NO)
        self.tree.heading("personID", text="ID", anchor=tk.W)

        self.tree.column("passportDataID", width=0, stretch=tk.NO)
        self.tree.heading("passportDataID", text="ID", anchor=tk.W)

        for document in documents: 
            self.tree.insert("", tk.END, values=document)

    def clearTable(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def giveId(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return None
           
        else:
            selected_item = selected_items[0]
            self.documentId = self.tree.item(selected_item)['values'][0]
            return self.documentId

    
    
        



