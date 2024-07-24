from aifc import Error
import tkinter as tk
from tkinter import ttk, messagebox
from InteractionWithTheDatabase import InteractionWithTheDatabase

class SearchUsers():
    def __init__(self, root):
        self.root = root
        self.eSearchFullName = None
        self.eSearchSeriesNumber = None
        self.eSearchStreet = None
        
    def displayingTheDesiredUser(self):
        titleSearch = tk.Label(self.root, text="Поиск:", font='Times 10')
        titleSearch.place(relx=0.1, rely=0.06, anchor="w")

        titleFullName = tk.Label(self.root, text="ФИО", font='Times 10')
        titleFullName.place(relx=0.25, rely=0.04, anchor="w")

        self.eSearchFullName = tk.Entry(self.root)
        self.eSearchFullName.place(relx=0.2, rely=0.06, anchor="w")

        titleSeriesNumber = tk.Label(self.root, text="Серия и номер", font='Times 10')
        titleSeriesNumber.place(relx=0.42, rely=0.04, anchor="w")

        self.eSearchSeriesNumber = tk.Entry(self.root)
        self.eSearchSeriesNumber.place(relx=0.4, rely=0.06, anchor="w")

        titleStreet = tk.Label(self.root, text="Улица", font='Times 10')
        titleStreet.place(relx=0.65, rely=0.04, anchor="w")

        self.eSearchStreet = tk.Entry(self.root)
        self.eSearchStreet.place(relx=0.6, rely=0.06, anchor="w")

        self.eSearchFullName.insert(0, "")
        self.eSearchSeriesNumber.insert(0, "")
        self.eSearchStreet.insert(0, "")

    
    def outputResults(self):

        def normalize_input(input_string):
            input_string = input_string.strip()
            words = input_string.split()
            normalized_string = " ".join(words)
            return normalized_string

        fullName = self.eSearchFullName.get()
        normalized_stringFullName = normalize_input(fullName)
        divisionFullName = normalized_stringFullName.split(" ")

        number = self.eSearchSeriesNumber.get()
        normalized_stringNumber = normalize_input(number)
        divisionNumber = normalized_stringNumber.split(" ")

        street = self.eSearchStreet.get()
        normalized_stringStreet = normalize_input(street)
        divisionStreet = normalized_stringStreet.split(" ")

        interactionWithTheDatabase = InteractionWithTheDatabase('localhost', 'main', 5432, "postgres", '123')
        interactionWithTheDatabase.connectionToDatabase()

        if not fullName.strip() or not number.strip() or not street.strip():
            if not fullName.strip():
                userSearch = []
            else:
                if len(divisionFullName) == 3:
                    userSearch = interactionWithTheDatabase.dataSearchFullName(divisionFullName[0], divisionFullName[1], divisionFullName[2])
                else:
                    userSearch = interactionWithTheDatabase.dataSearchFullNameError(divisionFullName)
                
            if not number.strip():
                seriesNumber = []
            else:
                if len(divisionNumber) == 2:
                    seriesNumber = interactionWithTheDatabase.dataSearchSeriesNumber(divisionNumber[0],divisionNumber[1])
                else:
                    seriesNumber = interactionWithTheDatabase.dataSearchSeriesNumberError(divisionNumber)
            
            if not street.strip():
                street = []
            else:
                street = interactionWithTheDatabase.dataSearchStreet(divisionStreet[0])
            interactionWithTheDatabase.closeConnection()
            arr = []
            arr.append([userSearch, seriesNumber, street])
            return arr
                
        else:
            userSearch = interactionWithTheDatabase.dataSearchFullName(divisionFullName)
            if len(divisionNumber) != 2:
                divisionNumber.append('')
            seriesNumber = interactionWithTheDatabase.dataSearchSeriesNumber(divisionNumber[0],divisionNumber[1])
            street = interactionWithTheDatabase.dataSearchStreet(divisionStreet[0])
            interactionWithTheDatabase.closeConnection()
            arr = []
            arr.append([userSearch, seriesNumber, street])
            return arr

        