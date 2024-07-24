import tkinter as tk
from tkinter import NW, StringVar, ttk, messagebox
from InteractionWithTheDatabase import InteractionWithTheDatabase
from tkcalendar import DateEntry
from SearchUsers import SearchUsers
from fpdf import FPDF

class CustomButton():
    def __init__(self, relx, rely, text, root, userTable, documentsTable, addressTable,searchUsers):
        self.relx = relx
        self.rely = rely
        self.text = text
        self.root = root
        self.userTable = userTable
        self.documentsTable = documentsTable
        self.addressTable = addressTable
        self.searchUsers = searchUsers
        
    def deleteUser(self):
        person_id = self.userTable.giveId()

        if person_id == None:
            messagebox.showinfo("Предупреждение", message="Перед удалением нужно выбрать пользователя")
            return
        
        result = messagebox.askyesno(title="Удаление", message="Вы уверены, что хотите удалить пользователя?")
        if result:
            
            person_id = self.userTable.giveId()

            interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
            interactionWithTheDatabase.connectionToDatabase()
            interactionWithTheDatabase.deletionPerson(person_id)
            interactionWithTheDatabase.closeConnection()
            messagebox.showinfo("Успех", message="Пользователь успешно удален")

            self.userTable.tableOutput()
            self.documentsTable.tableOutput()  
            self.addressTable.tableOutput()
            
        else:
            messagebox.showinfo("Удаление отменено", "Удаление пользователя отменено.") 

    def changeUser(self):

        person_id = self.userTable.giveId()
        if person_id == None:
            messagebox.showinfo("Предупреждение", message="Перед изменением нужно выбрать пользователя")
            return

        new_window = tk.Toplevel()
        new_window.geometry('350x200')
        new_window.title("Отдельное окно")

        titleEFirstName = tk.Label(new_window, text="Имя:", font='Times 10')
        titleEFirstName.place(relx=0, rely=0.07, anchor="w")

        titleESecondName = tk.Label(new_window, text="Фамилия:", font='Times 10')
        titleESecondName.place(relx=0, rely=0.23, anchor="w")

        titleEGender = tk.Label(new_window, text="Отчество:", font='Times 10')
        titleEGender.place(relx=0, rely=0.39, anchor="w")

        titleESurname = tk.Label(new_window, text="Пол:", font='Times 10')
        titleESurname.place(relx=0, rely=0.55, anchor="w")

        titleEDateOfBirth = tk.Label(new_window, text="Дата рождения:", font='Times 10')
        titleEDateOfBirth.place(relx=0, rely=0.71, anchor="w")

        eFirstName = tk.Entry(new_window)
        eFirstName.place(x=100, y=8, width=200)
        eSecondName = tk.Entry(new_window)
        eSecondName.place(x=100, y=40, width=200)
        eGender = tk.Entry(new_window)
        eGender.place(x=100, y=70, width=200)
        eSurname = tk.Entry(new_window)
        eSurname.place(x=100, y=102, width=200)
        eDateOfBirth = DateEntry(new_window, width=16, background='darkblue', foreground='white', borderwridth=2)
        
        eDateOfBirth.place(x=100, y=132, width=200)

        eDateOfBirth.delete(0, "end")
        
        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        person = interactionWithTheDatabase.displayingDataOfSpecificEmployee(person_id)
        interactionWithTheDatabase.closeConnection()

        eFirstName.insert(0, person[0][1])
        eSecondName.insert(0, person[0][2])
        eSurname.insert(0, person[0][3])
        eGender.insert(0, person[0][4])
        eDateOfBirth.insert(0, person[0][5])

        def change():
            selected_itemFirstName = eFirstName.get().strip()
            selected_itemSecondName = eSecondName.get().strip()
            selected_itemSurname = eSurname.get().strip()
            selected_itemGender = eGender.get().strip()
            selected_itemDateOfBirth = eDateOfBirth.get().strip()

            if not selected_itemFirstName or not selected_itemSecondName or not selected_itemSurname or not selected_itemGender or not selected_itemDateOfBirth:
                messagebox.showinfo("Ошибка", message="Одно из полей не введено")
            else:
                interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
                interactionWithTheDatabase.connectionToDatabase()
                interactionWithTheDatabase.changePerson(selected_itemFirstName, selected_itemSecondName, selected_itemGender, selected_itemSurname, selected_itemDateOfBirth, person_id)
                interactionWithTheDatabase.closeConnection()
                
                messagebox.showinfo("Успех", message="Пользователь успешно изменен")
                self.userTable.tableOutput()

        button = tk.Button(new_window, text="Сохранить изменение", command=change)
        button.place(relx=0.5, rely=0.9, anchor="center")

    def addUser(self):
        new_window = tk.Toplevel()
        new_window.geometry('350x200')
        new_window.title("Отдельное окно")

        titleEFirstName = tk.Label(new_window, text="Имя:", font='Times 10')
        titleEFirstName.place(relx=0, rely=0.07, anchor="w")

        titleESecondName = tk.Label(new_window, text="Фамилия:", font='Times 10')
        titleESecondName.place(relx=0, rely=0.23, anchor="w")

        titleEGender = tk.Label(new_window, text="Отчество:", font='Times 10')
        titleEGender.place(relx=0, rely=0.39, anchor="w")

        titleESurname = tk.Label(new_window, text="Пол:", font='Times 10')
        titleESurname.place(relx=0, rely=0.55, anchor="w")

        titleEDateOfBirth = tk.Label(new_window, text="Дата рождения:", font='Times 10')
        titleEDateOfBirth.place(relx=0, rely=0.71, anchor="w")

        

        eFirstName = tk.Entry(new_window)
        eFirstName.place(x=100, y=8, width=200)
        eSecondName = tk.Entry(new_window)
        eSecondName.place(x=100, y=40, width=200)
        eGender = tk.Entry(new_window)
        eGender.place(x=100, y=70, width=200)
        eSurname = tk.Entry(new_window)
        eSurname.place(x=100, y=102, width=200)
        eDateOfBirth = DateEntry(new_window, width=16, background='darkblue', foreground='white', borderwridth=2)
        eDateOfBirth.place(x=100, y=132, width=200)
        eDateOfBirth.delete(0, "end")

        eFirstName.insert(0, "")
        eSecondName.insert(0, "")
        eSurname.insert(0, "")
        eGender.insert(0, "")
        eDateOfBirth.insert(0, "")

        def add():
            selected_itemFirstName = eFirstName.get().strip()
            selected_itemSecondName = eSecondName.get().strip()
            selected_itemSurname = eSurname.get().strip()
            selected_itemGender = eGender.get().strip()
            selected_itemDateOfBirth = eDateOfBirth.get().strip()

            if not selected_itemFirstName or not selected_itemSecondName or not selected_itemSurname or not selected_itemGender or not selected_itemDateOfBirth:
                messagebox.showinfo("Ошибка", message="Одно из полей не введено")
            else:
                interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
                interactionWithTheDatabase.connectionToDatabase()
                interactionWithTheDatabase.addPerson(selected_itemFirstName, selected_itemSecondName, selected_itemSurname, selected_itemGender, selected_itemDateOfBirth)
                interactionWithTheDatabase.closeConnection()
                
                
                eFirstName.delete(0, tk.END)
                eSecondName.delete(0, tk.END)
                eSurname.delete(0, tk.END)
                eGender.delete(0, tk.END)
                eDateOfBirth.delete(0, tk.END)
                messagebox.showinfo("Успех", message="Пользователь успешно добавлен")
                self.userTable.tableOutput()

        button = tk.Button(new_window, text="Добавить", command=add)
        button.place(relx=0.5, rely=0.9, anchor="center")

    def addDocument(self):

        person_id = self.userTable.giveId()
        if person_id == None:
            messagebox.showinfo("Предупреждение", message="Перед изменением нужно выбрать пользователя")
            return

        new_window = tk.Toplevel()
        new_window.geometry('350x200')
        new_window.title("Отдельное окно")

        titleEDocumentationReferenceID = tk.Label(new_window, text="Тип документа:", font='Times 10')
        titleEDocumentationReferenceID.place(relx=0, rely=0.07, anchor="w")

        titleESerialNumber = tk.Label(new_window, text="Серия:", font='Times 10')
        titleESerialNumber.place(relx=0, rely=0.23, anchor="w")

        titleENumberPD = tk.Label(new_window, text="Номер:", font='Times 10')
        titleENumberPD.place(relx=0, rely=0.39, anchor="w")

        titleEDateOfIssue = tk.Label(new_window, text="Дата получения:", font='Times 10')
        titleEDateOfIssue.place(relx=0, rely=0.55, anchor="w")

        

        titleEIssuedByWhom = tk.Label(new_window, text="Кем выдан:", font='Times 10')
        titleEIssuedByWhom.place(relx=0, rely=0.71, anchor="w")

        eSerialNumber = tk.Entry(new_window)
        eSerialNumber.place(x=100, y=40, width=200)
        eNumberPD = tk.Entry(new_window)
        eNumberPD.place(x=100, y=70, width=200)
        eDateOfIssue = DateEntry(new_window, width=16, background='darkblue', foreground='white', borderwridth=2)
        eDateOfIssue.place(x=100, y=102, width=200)
        eDateOfIssue.delete(0, "end")
        eIssuedByWhom = tk.Entry(new_window)
        eIssuedByWhom.place(x=100, y=132, width=200)

        eSerialNumber.insert(0, "")
        eNumberPD.insert(0, "")
        eDateOfIssue.insert(0, "")
        eIssuedByWhom.insert(0, "")

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        typeOfDocuments = interactionWithTheDatabase.receivingAllTypesOfDocuments()
        
        options = [i[0] for i in typeOfDocuments]
        comboBoxDucument = ttk.Combobox(new_window,justify="center",state="readonly")
        comboBoxDucument["values"] = tuple(options)
        comboBoxDucument.place(x=100, y=8, width=200)

        def add():
            selected_itemDocumentationReferenceID = comboBoxDucument.current() + 1 

            selected_itemSerialNumber = eSerialNumber.get().strip()
            selected_itemNumberPD = eNumberPD.get().strip()
            selected_itemDateOfIssue = eDateOfIssue.get().strip()
            selected_itemIssuedByWhom = eIssuedByWhom.get().strip()

            if not  selected_itemDocumentationReferenceID > 0 or not selected_itemSerialNumber or not selected_itemNumberPD or not selected_itemDateOfIssue or not selected_itemIssuedByWhom:
                messagebox.showinfo("Ошибка", message="Одно из полей не введено")
                interactionWithTheDatabase.closeConnection()
                
            else:
                interactionWithTheDatabase.addDocument(selected_itemDocumentationReferenceID, selected_itemSerialNumber, selected_itemNumberPD, selected_itemDateOfIssue, selected_itemIssuedByWhom, person_id)
              
                eSerialNumber.delete(0, tk.END)
                eNumberPD.delete(0, tk.END)
                eDateOfIssue.delete(0, tk.END)
                eIssuedByWhom.delete(0, tk.END)
                messagebox.showinfo("Успех", message="Документ успешно добавлен")
                self.documentsTable.tableOutput()
                interactionWithTheDatabase.closeConnection()

        button = tk.Button(new_window, text="Добавить", command=add)
        button.place(relx=0.5, rely=0.9, anchor="center")

    def deletionDocument(self):
        documentsId = self.documentsTable.giveId()
        

        if documentsId == None:
            messagebox.showinfo("Предупреждение", message="Перед удалением нужно выбрать документ")
            return
        
        result = messagebox.askyesno(title="Удаление", message="Вы уверены, что хотите удалить документ?")
        if result:
            
            

            interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
            interactionWithTheDatabase.connectionToDatabase()
            interactionWithTheDatabase.deletionDocument(documentsId)
            interactionWithTheDatabase.closeConnection()
            messagebox.showinfo("Успех", message="Документ успешно удален")
            self.documentsTable.tableOutput()
            
        else:
            messagebox.showinfo("Удаление отменено", "Удаление документа отменено.") 
    
    def changeDocument(self):
        person_id = self.userTable.giveId()
        documentsId = self.documentsTable.giveId()
        if documentsId == None:
            messagebox.showinfo("Предупреждение", message="Перед изменением нужно выбрать документ")
            return

        new_window = tk.Toplevel()
        new_window.geometry('350x200')
        new_window.title("Отдельное окно")

        titleEDocumentationReferenceID = tk.Label(new_window, text="Тип документа:", font='Times 10')
        titleEDocumentationReferenceID.place(relx=0, rely=0.07, anchor="w")

        titleESerialNumber = tk.Label(new_window, text="Серия:", font='Times 10')
        titleESerialNumber.place(relx=0, rely=0.23, anchor="w")

        titleENumberPD = tk.Label(new_window, text="Номер:", font='Times 10')
        titleENumberPD.place(relx=0, rely=0.39, anchor="w")

        titleEDateOfIssue = tk.Label(new_window, text="Дата получения:", font='Times 10')
        titleEDateOfIssue.place(relx=0, rely=0.55, anchor="w")

        titleEIssuedByWhom = tk.Label(new_window, text="Кем выдан:", font='Times 10')
        titleEIssuedByWhom.place(relx=0, rely=0.71, anchor="w")

        
        titleESerialNumber = tk.Entry(new_window)
        titleESerialNumber.place(x=100, y=40, width=200)
        titleENumberPD = tk.Entry(new_window)
        titleENumberPD.place(x=100, y=70, width=200)

        titleEDateOfIssue = DateEntry(new_window, width=16, background='darkblue', foreground='white', borderwridth=2)
        titleEDateOfIssue.place(x=100, y=102, width=200)
        titleEDateOfIssue.delete(0,"end")

        titleEIssuedByWhom = tk.Entry(new_window)
        titleEIssuedByWhom.place(x=100, y=132, width=200)

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        typeOfDocuments = interactionWithTheDatabase.receivingAllTypesOfDocuments()
        document = interactionWithTheDatabase.displayingDataOfSpecificDocument(documentsId)
        

        options = [i[0] for i in typeOfDocuments]
        comboBoxDucument = ttk.Combobox(new_window,justify="center",state="readonly")
        comboBoxDucument["values"] = tuple(options)
        comboBoxDucument.place(x=100, y=8, width=200)

        
        titleESerialNumber.insert(0, document[0][3])
        titleENumberPD.insert(0, document[0][4])
        titleEDateOfIssue.insert(0, document[0][5])
        titleEIssuedByWhom.insert(0, document[0][6])

        def change():
            selected_itemDocumentationReferenceID = comboBoxDucument.current() + 1 
            selected_itemESerialNumber = titleESerialNumber.get().strip()
            selected_itemENumberPD = titleENumberPD.get().strip()
            selected_itemEDateOfIssue = titleEDateOfIssue.get().strip()
            selected_itemEIssuedByWhom = titleEIssuedByWhom.get().strip()

            if not selected_itemDocumentationReferenceID > 0 or not selected_itemESerialNumber or not selected_itemENumberPD or not selected_itemEDateOfIssue or not selected_itemEIssuedByWhom:
                messagebox.showinfo("Ошибка", message="Одно из полей не введено")
            else:
                interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
                interactionWithTheDatabase.connectionToDatabase()
                interactionWithTheDatabase.changeDocument(person_id, selected_itemDocumentationReferenceID, selected_itemESerialNumber, selected_itemENumberPD, selected_itemEDateOfIssue, selected_itemEIssuedByWhom, documentsId)
                interactionWithTheDatabase.closeConnection()
                
                messagebox.showinfo("Успех", message="Пользователь успешно изменен")
                self.documentsTable.tableOutput()

        button = tk.Button(new_window, text="Сохранить изменение", command=change)
        button.place(relx=0.5, rely=0.9, anchor="center")

    def addAddress(self):
        person_id = self.userTable.giveId()
        if person_id == None:
            messagebox.showinfo("Предупреждение", message="Перед изменением нужно выбрать пользователя")
            return

        new_window = tk.Toplevel()
        new_window.geometry('350x200')
        new_window.title("Отдельное окно")

        typeOfAdressID = tk.Label(new_window, text="Тип адреса:", font='Times 10')
        typeOfAdressID.place(relx=0, rely=0.07, anchor="w")

        city = tk.Label(new_window, text="Город", font='Times 10')
        city.place(relx=0, rely=0.23, anchor="w")

        street = tk.Label(new_window, text="Улица", font='Times 10')
        street.place(relx=0, rely=0.39, anchor="w")

        apartmentNumber = tk.Label(new_window, text="Номер квартиры:", font='Times 10')
        apartmentNumber.place(relx=0, rely=0.55, anchor="w")
       
        eCity = tk.Entry(new_window)
        eCity.place(x=100, y=40, width=200)
        eStreet = tk.Entry(new_window)
        eStreet.place(x=100, y=70, width=200)
        eApartmentNumber = tk.Entry(new_window)
        eApartmentNumber.place(x=100, y=102, width=200)
    
        eCity.insert(0, "")
        eStreet.insert(0, "")
        eApartmentNumber.insert(0, "")

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        typeOfAdress = interactionWithTheDatabase.receivingAllTypesOfAdress()

        options = [i[0] for i in typeOfAdress]
        comboBoxAdress = ttk.Combobox(new_window,justify="center",state="readonly")
        comboBoxAdress["values"] = tuple(options)
        comboBoxAdress.place(x=100, y=8, width=200)

        def add():
            selected_itemTypeOfAdressID = comboBoxAdress.current() + 1 

            selected_itemECity = eCity.get().strip()
            selected_itemEStreet = eStreet.get().strip()
            selected_itemEApartmentNumber = eApartmentNumber.get().strip()
            

            if not  selected_itemTypeOfAdressID > 0 or not selected_itemECity or not selected_itemEStreet or not selected_itemEApartmentNumber:
                messagebox.showinfo("Ошибка", message="Одно из полей не введено")
                interactionWithTheDatabase.closeConnection()
            else:
                interactionWithTheDatabase.addAdress(selected_itemECity, selected_itemEStreet, selected_itemEApartmentNumber, person_id, selected_itemTypeOfAdressID)
              
                eCity.delete(0, tk.END)
                eStreet.delete(0, tk.END)
                eApartmentNumber.delete(0, tk.END)
                messagebox.showinfo("Успех", message="Адрес успешно добавлен")
                self.addressTable.tableOutput()  
                interactionWithTheDatabase.closeConnection()

        button = tk.Button(new_window, text="Добавить", command=add)
        button.place(relx=0.5, rely=0.9, anchor="center")

    def deletionAddress(self):
        adessId = self.addressTable.giveId()
        
        if adessId == None:
            messagebox.showinfo("Предупреждение", message="Перед удалением нужно выбрать ардес")
            return
        
        result = messagebox.askyesno(title="Удаление", message="Вы уверены, что хотите удалить данный адрес?")
        if result:
            interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
            interactionWithTheDatabase.connectionToDatabase()
            interactionWithTheDatabase.deletionAdres(adessId)
            interactionWithTheDatabase.closeConnection()
            messagebox.showinfo("Успех", message="Адрес успешно удален")
            self.addressTable.tableOutput()
            
        else:
            interactionWithTheDatabase.closeConnection()
            messagebox.showinfo("Удаление отменено", "Удаление адреса отменено.") 

    def changeAddress(self):
        person_id = self.userTable.giveId()
        adessId = self.addressTable.giveId()
        if adessId == None:
            messagebox.showinfo("Предупреждение", message="Перед изменением нужно выбрать адрес")
            return

        new_window = tk.Toplevel()
        new_window.geometry('350x200')
        new_window.title("Отдельное окно")

        typeOfAdressID = tk.Label(new_window, text="Тип адреса:", font='Times 10')
        typeOfAdressID.place(relx=0, rely=0.07, anchor="w")

        city = tk.Label(new_window, text="Город", font='Times 10')
        city.place(relx=0, rely=0.23, anchor="w")

        street = tk.Label(new_window, text="Улица", font='Times 10')
        street.place(relx=0, rely=0.39, anchor="w")

        apartmentNumber = tk.Label(new_window, text="Номер квартиры:", font='Times 10')
        apartmentNumber.place(relx=0, rely=0.55, anchor="w")
       
        eCity = tk.Entry(new_window)
        eCity.place(x=100, y=40, width=200)
        eStreet = tk.Entry(new_window)
        eStreet.place(x=100, y=70, width=200)
        eApartmentNumber = tk.Entry(new_window)
        eApartmentNumber.place(x=100, y=102, width=200)
    
        

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        typeOfAdress = interactionWithTheDatabase.receivingAllTypesOfAdress()
        adress = interactionWithTheDatabase.displayingDataOfSpecificAdress(adessId)

        options = [i[0] for i in typeOfAdress]
        comboBoxAdress = ttk.Combobox(new_window,justify="center",state="readonly")
        comboBoxAdress["values"] = tuple(options)
        comboBoxAdress.place(x=100, y=8, width=200)

        eCity.insert(0, adress[0][1])
        eStreet.insert(0, adress[0][2])
        eApartmentNumber.insert(0, adress[0][3])

        def change():
            selected_itemTypeOfAdressID = comboBoxAdress.current() + 1 

            selected_itemECity = eCity.get().strip()
            selected_itemEStreet = eStreet.get().strip()
            selected_itemEApartmentNumber = eApartmentNumber.get().strip()

            if not selected_itemTypeOfAdressID > 0 or not selected_itemECity or not selected_itemEStreet or not selected_itemEApartmentNumber:
                messagebox.showinfo("Ошибка", message="Одно из полей не введено")
            else:
                interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
                interactionWithTheDatabase.connectionToDatabase()
                interactionWithTheDatabase.changeAdress(selected_itemECity, selected_itemEStreet, selected_itemEApartmentNumber ,person_id, selected_itemTypeOfAdressID,adessId)
                interactionWithTheDatabase.closeConnection()
                
                messagebox.showinfo("Успех", message="Адрес успешно изменен")
                self.addressTable.tableOutput()

        button = tk.Button(new_window, text="Сохранить изменение", command=change)
        button.place(relx=0.5, rely=0.9, anchor="center")

    def quest(self):
        searchUsers = self.searchUsers.outputResults()
        selected_itemFullName = searchUsers[0]
        c = 0
        count = 0
        for i in selected_itemFullName:
            c += 1
            if i:
                count += 1
                if c == 1:
                    self.userTable.tableOutputError(selected_itemFullName)
                elif c == 2:
                    self.userTable.tableOutputError2(selected_itemFullName)
                elif c == 3:
                    self.userTable.tableOutputError3(selected_itemFullName)
            else:
                if count == 0:
                    self.userTable.tableOutput()

    def savePDF(self):
        pdf = FPDF()
        pdf.add_page() 
        pdf.add_font('Arial','','fonts/ARIAL.TTF.',uni=True)    
        pdf.set_font('Arial', size=25)  

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()
        persons = interactionWithTheDatabase.weAskForEmployees()
        for i in persons:
            pdf.cell(200, 10, txt=str(i), ln=1,align="C")

        pdf.output('pdfTest.pdf')
        
    def pressingAdd(self):
        button = tk.Button(self.root, text=self.text, command=self.addUser)
        button.place(relx=self.relx, rely=self.rely, anchor="center")

    def pressingDelete(self):
        button = tk.Button(self.root, text=self.text, command=self.deleteUser)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def pressingСhange(self):   
        button = tk.Button(self.root, text=self.text, command=self.changeUser)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def documentAdd(self):
        button = tk.Button(self.root, text=self.text, command=self.addDocument)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def documentDeletion(self):
        button = tk.Button(self.root, text=self.text, command=self.deletionDocument)
        button.place(relx=self.relx, rely=self.rely, anchor="center")

    def documentChange(self):
        button = tk.Button(self.root, text=self.text, command=self.changeDocument)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def adressAdd(self):
        button = tk.Button(self.root, text=self.text, command=self.addAddress)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def adressDeletion(self):
        button = tk.Button(self.root, text=self.text, command=self.deletionAddress)
        button.place(relx=self.relx, rely=self.rely, anchor="center")

    def adressChange(self):
        button = tk.Button(self.root, text=self.text, command=self.changeAddress)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def searchUser(self):
        button = tk.Button(self.root, text=self.text, command= self.quest)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
    
    def saveUser(self):
        button = tk.Button(self.root, text=self.text, command= self.savePDF)
        button.place(relx=self.relx, rely=self.rely, anchor="center")
        

