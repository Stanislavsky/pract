from aifc import Error
from sqlite3 import OperationalError
import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox



class InteractionWithTheDatabase():

    def __init__(self, host, database, port, user, password):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.cursor = None
        self.conn = None
    
    def connectionToDatabase(self):
        try:
            self.conn = psycopg2.connect(
                host = self.host,
                database = self.database,
                port = self.port,
                user = self.user,
                password = self.password
            )
            self.cursor = self.conn.cursor()
            
        except OperationalError as e:
            print(f"erroe:{e}")

    def weAskForEmployees(self):
        try:
            self.cursor.execute('SELECT personID, firstName, secondName, surname, gender, dateOfBirth FROM person')
            return self.cursor.fetchall()
        except Error as e:
            print(f"erroe:{e}")
            return[]

    def displayingDataOfSpecificEmployee(self, person_id):
        try:
            self.cursor.execute('SELECT * FROM person WHERE personID = %s', (person_id,))
            result = self.cursor.fetchall()
            return result

        except Error as e:
            print(f"error:{e}")
            return[]
    
    def displayingDataOfSpecificDocument(self, documentsId):
        try:
            self.cursor.execute('SELECT * FROM passportData WHERE passportDataID = %s', (documentsId,))
            result = self.cursor.fetchall()
            return result

        except Error as e:
            print(f"error:{e}")
            return[]
    
    def displayingDataOfSpecificAdress(self, adessId):
        try:
            self.cursor.execute('SELECT * FROM address WHERE addressID = %s', (adessId,))
            result = self.cursor.fetchall()
            return result

        except Error as e:
            print(f"error:{e}")
            return[]

    def documentOutput(self, person_id):
        try:
            self.cursor.execute('SELECT * FROM passportData WHERE personID = %s', (person_id,))
            passport_data = self.cursor.fetchall()
            result = []
            for passport in passport_data:
                self.cursor.execute('SELECT typeOfDocument FROM documentationReference WHERE documentationReferenceID = %s', (passport[2],))
                passport = list(passport)
                passport[2] = self.cursor.fetchone()[0]
                result.append(passport)
            return result

        except Error as e:
            print(f"error:{e}")
            return[]
        
    def addressOutput(self, person_id):
        try:
            self.cursor.execute('SELECT * FROM address WHERE personID = %s', (person_id,))
            typeOfAdress_data = self.cursor.fetchall()
            result = []
            for adress in typeOfAdress_data:
                self.cursor.execute('SELECT typeOfAdress FROM typeOfAdress WHERE typeOfAdressID = %s', (adress[5],))
                adress = list(adress)
                adress[5] = self.cursor.fetchone()[0] 
                result.append(adress)
            return result
        
        except Error as e:
            print(f"error {e}")
            return[]
    
    def addPerson(self, selected_itemFirstName, selected_itemSecondName, selected_itemSurname, selected_itemGender, selected_itemDateOfBirth):
        try:
            self.cursor.execute(''' INSERT INTO person (firstName, secondName, gender, surname, dateOfBirth) VALUES(%s,%s,%s,%s,%s) ''',
                            (selected_itemFirstName, selected_itemSecondName, selected_itemSurname, selected_itemGender, selected_itemDateOfBirth))
            self.conn.commit()

        except Error as e:
            print(f"error {e}")
            return[]
        
    def addDocument(self, selected_itemDocumentationReferenceID, selected_itemSerialNumber, selected_itemNumberPD, selected_itemDateOfIssue, selected_itemIssuedByWhom, person_id):
        try:
            self.cursor.execute(''' INSERT INTO passportData ( documentationReferenceID, serialNumber, numberPD, dateOfIssue, issuedByWhom, personID) VALUES(%s,%s,%s,%s,%s,%s)''',
                (selected_itemDocumentationReferenceID, selected_itemSerialNumber, selected_itemNumberPD, selected_itemDateOfIssue, selected_itemIssuedByWhom, person_id))
            self.conn.commit()

        except Error as e:
            print(f"error {e}")
            return[]
    
    def addAdress(self,selected_itemECity,selected_itemEStreet,selected_itemEApartmentNumber, person_id,selected_itemTypeOfAdressID):
        try:
            self.cursor.execute(''' INSERT INTO address ( city, street, apartmentNumber, personID, typeOfAdressID) VALUES(%s,%s,%s,%s,%s)''',
                (selected_itemECity, selected_itemEStreet, selected_itemEApartmentNumber, person_id, selected_itemTypeOfAdressID))
            self.conn.commit()

        except Error as e:
            print(f"error {e}")
            return[]
    
    def receivingAllTypesOfDocuments(self):
        try:
            self.cursor.execute('SELECT typeOfDocument FROM documentationReference ORDER BY documentationreferenceid')
            passport_data = self.cursor.fetchall()
            return passport_data
        
        except Error as e:
            print(f"error {e}")
            return[]
    
    def receivingAllTypesOfAdress(self):
        try:
            self.cursor.execute('SELECT typeOfAdress FROM typeOfAdress ORDER BY typeOfAdressID')
            adress_data = self.cursor.fetchall()
            return adress_data
        
        except Error as e:
            print(f"error {e}")
            return[]
        
    def changePerson(self, selected_itemFirstName, selected_itemSecondName, selected_itemSurname, selected_itemGender, selected_itemDateOfBirth, person_id):
        try:
            self.cursor.execute(''' UPDATE person SET firstName = %s,  secondName = %s, gender = %s, surname = %s, dateOfBirth = %s WHERE personID = %s''',
                (selected_itemFirstName, selected_itemSecondName,  selected_itemGender, selected_itemSurname, selected_itemDateOfBirth, person_id))
            self.conn.commit()

        except Error as e:
            print(f"error {e}")
            return[]
    
    def changeDocument(self,personID, selected_itemDocumentationReferenceID, selected_itemESerialNumber, selected_itemENumberPD, selected_itemEDateOfIssue, selected_itemEIssuedByWhom, documentsId):
        try:
            self.cursor.execute(''' UPDATE passportData SET personID = %s, documentationReferenceID = %s,  serialNumber = %s, numberPD = %s, dateOfIssue = %s, issuedByWhom = %s WHERE passportDataID = %s''',
                (personID, selected_itemDocumentationReferenceID, selected_itemESerialNumber,  selected_itemENumberPD, selected_itemEDateOfIssue, selected_itemEIssuedByWhom, documentsId))
            self.conn.commit()

        except Error as e:
            print(f"error {e}")
            return[]
    
    def changeAdress(self,selected_itemECity, selected_itemEStreet, selected_itemEApartmentNumber, person_id, selected_itemTypeOfAdressID, adessId):
        try:
            self.cursor.execute(''' UPDATE address SET  city = %s,  street = %s, apartmentNumber = %s, personID = %s, typeOfAdressID = %s WHERE addressID = %s''',
                (selected_itemECity, selected_itemEStreet, selected_itemEApartmentNumber,  person_id, selected_itemTypeOfAdressID, adessId))
            self.conn.commit()

        except Error as e:
            print(f"error {e}")
            return[]

    def deletionPerson(self, person_id):
        self.cursor.execute('DELETE FROM person WHERE personID = %s', (person_id,))
        self.conn.commit()

    def deletionDocument(self,documentsId):
        self.cursor.execute('DELETE FROM passportData WHERE passportDataID = %s', (documentsId,))
        self.conn.commit()
    
    def deletionAdres(self,adessId):
        self.cursor.execute('DELETE FROM address WHERE addressID = %s', (adessId,))
        self.conn.commit()
    
    def dataSearchFullName(self, full_name):

        placeholders = ', '.join(['%s'] * len(full_name))  
        sql = f"SELECT * FROM person WHERE firstName IN ({placeholders}) OR secondName IN ({placeholders}) OR surname IN ({placeholders})"  
        full_name_list = full_name
        while len(full_name) != 3:
            full_name.append('')
        self.cursor.execute(sql, tuple(full_name))  
        results = self.cursor.fetchall()
        return results
    
    def dataSearchFullNameError(self, normalized_stringNumber):
        
        firstName = normalized_stringNumber[0] + '%'

        self.cursor.execute(''' 
            SELECT * FROM person  
                WHERE  
                    firstName LIKE %s 
                    OR secondName LIKE %s
                    OR surname LIKE %s;''',(firstName, firstName, firstName)
        )
        results = self.cursor.fetchall()
        return results
        
    def dataSearchSeriesNumber(self, divisionNumber1, divisionNumber2):

        divisionNumber1_pattern = divisionNumber1 + "%"
        divisionNumber2_pattern = divisionNumber2 + "%"
        
        self.cursor.execute(''' 
            SELECT * FROM passportData  
                WHERE  
                    CAST(serialNumber AS TEXT) LIKE %s  
                    AND CAST(numberPD AS TEXT) LIKE %s;''',(divisionNumber1_pattern, divisionNumber2_pattern)
        )
        results = self.cursor.fetchall()
        return results
    

    def dataSearchSeriesNumberError(self, divisionNumber):

        number = divisionNumber[0] + "%"

        self.cursor.execute(''' 
            SELECT * FROM passportData  
                WHERE  
                    CAST(serialNumber AS TEXT) LIKE %s 
                    OR CAST(numberPD AS TEXT) LIKE %s;''',(number, number)
        )
        results = self.cursor.fetchall()
        return results


    
    def dataSearchStreet(self, divisionStreet):

        divisionStreet_pattern = divisionStreet + "%"

        self.cursor.execute(''' 
            SELECT * FROM address  
                WHERE  
                    street LIKE %s;''',(divisionStreet_pattern,) 
        )
        results = self.cursor.fetchall()
        return results
    
    def weAskForEmployeesNecessary(self, persons):
        placeholders = ', '.join(['%s'] * len(persons))  
        sql = f"SELECT * FROM person WHERE personID IN ({placeholders})"  

        self.cursor.execute(sql, tuple(persons))  
        results = self.cursor.fetchall()
        return results
    
    def closeConnection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

