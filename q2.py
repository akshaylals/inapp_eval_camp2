from tokenize import String
import pyodbc
import functools
import re


class Utils:
    def getInt(*args):
        while True:
            try:
                val = int(input(*args))
            except:
                print('Invalid Input')
            else:
                return val
    
    def getString(*args):
        while True:
            val = input(*args)
            if val.strip() != '':
                return val
            else:
                print('Invalid Input')
                continue


class DBMS:
    def connect(func):
        @functools.wraps(func)
        def innerWrapper(*args):
            try:
                conn = pyodbc.connect(
                    'Driver={SQL Server};'
                    'Server=DESKTOP-4GIE4U2\SQLEXPRESS01;'
                    'Database=camp2_eval_q2;'
                    'Trusted_Connection=yes'
                )
            except:
                print('Connection error')
                exit(1)
            else:
                value = func(conn, *args)
                conn.commit()
                conn.close()
                return value
        return innerWrapper


class Patient:
    @property
    def name(self):
        return self.__name

    @property
    def gender(self):
        return self.__gender
    
    @property
    def age(self):
        return self.__age
    
    @property
    def blood(self):
        return self.__blood

    @name.setter
    def name(self, val):
        if isinstance(val, str):
            if val.strip() != '':
                self.__name = val.strip()
            else:
                raise Exception('Name cannot be blank')
        else:
            raise TypeError('Name should be String Type')
    
    @gender.setter
    def gender(self, val):
        if isinstance(val, str):
            if val.strip() != '':
                if val.strip() in ['M', 'F']:
                    self.__gender = val.strip()
                else:
                    raise Exception('Invalid option')
            else:
                raise Exception('Gender cannot be blank')
        else:
            raise TypeError('Gender should be String Type')

    @age.setter
    def age(self, val):
        if isinstance(val, int):
            if val > 0:
                self.__age = val
            else:
                raise Exception('Age should be above 0')
        else:
            raise TypeError('Age should be int Type')
    
    @blood.setter
    def blood(self, val):
        if isinstance(val, str):
            if val.strip() != '':
                if re.match(r'^(A|B|AB|O)[+-]$', val.strip()):
                    self.__blood = val.strip()
                else:
                    raise Exception('Invalid option')
            else:
                raise Exception('Blood type cannot be blank')
        else:
            raise TypeError('Blood type should be String Type')


class PMS(DBMS):
    @staticmethod
    @DBMS.connect
    def addPatient(conn: pyodbc.Connection):
        patient = Patient()
        while(True):
            try:
                patient.name = input('Enter name: ')
            except Exception as e:
                print(e)
            else:
                break

        while(True):
            try:
                patient.gender = input('Enter gender: ')
            except Exception as e:
                print(e)
            else:
                break
        
        while(True):
            try:
                patient.age = Utils.getInt('Enter age: ')
            except Exception as e:
                print(e)
            else:
                break
        
        while(True):
            try:
                patient.blood = input('Enter blood: ')
            except Exception as e:
                print(e)
            else:
                break
        
        curr = conn.cursor()
        curr.execute(
            'INSERT INTO patients VALUES (?, ?, ?, ?)',
            (patient.name, patient.gender, patient.age, patient.blood)
        )
        conn.commit()

    @staticmethod
    @DBMS.connect
    def updatePatient(conn: pyodbc.Connection):
        patient = Patient()
        id = Utils.getInt('Enter patient ID: ')
        curr = conn.cursor()
        curr.execute('SELECT * FROM patients WHERE patientId=?', (id))

        exists = False
        for id, name, gender, age, blood in curr.fetchall():
            print('\nID:', id)
            print('Name:', name)
            print('Gender:', gender)
            print('Age:', age)
            print('Blood:', blood)
            exists = True
        
        if not exists:
            print('Patient does not exist')

        while True:
            opt = Utils.getInt('''
            1. Name
            2. Gender
            3. Age
            4. Blood
            0. Back
            > ''')
            match opt:
                case 1:
                    while(True):
                        try:
                            patient.name = input('Enter name: ')
                        except Exception as e:
                            print(e)
                        else:
                            try:
                                curr.execute('UPDATE patients SET patientName=?', (patient.name))
                            except:
                                print('Error updating')
                            else:
                                print('Updated successfully')
                            break
                case 2:
                    while(True):
                        try:
                            patient.gender = input('Enter gender: ')
                        except Exception as e:
                            print(e)
                        else:
                            try:
                                curr.execute('UPDATE patients SET gender=?', (patient.gender))
                            except:
                                print('Error updating')
                            else:
                                print('Updated successfully')
                            break
                case 3:
                    while(True):
                        try:
                            patient.age = Utils.getInt('Enter age: ')
                        except Exception as e:
                            print(e)
                        else:
                            try:
                                curr.execute('UPDATE patients SET age=?', (patient.age))
                            except:
                                print('Error updating')
                            else:
                                print('Updated successfully')
                            break
                case 4:
                    while(True):
                        try:
                            patient.blood = input('Enter blood: ')
                        except Exception as e:
                            print(e)
                        else:
                            try:
                                curr.execute('UPDATE patients SET bloodGroup=?', (patient.blood))
                            except:
                                print('Error updating')
                            else:
                                print('Updated successfully')
                            break
                case 0: break
                case _: print('Invalid option')
        pass

    @staticmethod
    @DBMS.connect
    def deletePatient(conn: pyodbc.Connection):
        patient = Patient()
        while(True):
            try:
                patient.name = input('Enter name to search: ')
            except Exception as e:
                print(e)
            else:
                break
        
        curr = conn.cursor()
        curr.execute(
            'DELETE FROM patients WHERE patientName=?',
            (patient.name)
        )

        if curr.rowcount > 0:
            print('Successfully deleted')
        else:
            print(f'{patient.name} does not exist')

    @staticmethod
    @DBMS.connect
    def listPatients(conn: pyodbc.Connection):
        curr = conn.cursor()
        curr.execute('SELECT * FROM patients;')
        exists = False
        for id, name, gender, age, blood in curr.fetchall():
            print('\nID:', id)
            print('Name:', name)
            print('Gender:', gender)
            print('Age:', age)
            print('Blood:', blood)
            exists = True
        
        if not exists:
            print('No Patients')

    @staticmethod
    @DBMS.connect
    def searchPatient(conn: pyodbc.Connection):
        patient = Patient()
        while(True):
            try:
                patient.name = input('Enter name to search: ')
            except Exception as e:
                print(e)
            else:
                break
        curr = conn.cursor()
        curr.execute(
            'SELECT * FROM patients WHERE patientName LIKE ?;',
            (patient.name)
        )
        
        exists = False
        for id, name, gender, age, blood in curr.fetchall():
            print('\nID:', id)
            print('Name:', name)
            print('Gender:', gender)
            print('Age:', age)
            print('Blood:', blood)
            exists = True
        
        if not exists:
            print('Patient does not exist')


while (True):
    opt = Utils.getInt('''
    1. Add
    2. Update
    3. Delete
    4. List
    5. Search
    0. Exit
    > ''')
    match opt:
        case 0: break
        case 1: PMS.addPatient()
        case 2: PMS.updatePatient()
        case 3: PMS.deletePatient()
        case 4: PMS.listPatients()
        case 5: PMS.searchPatient()
        case _: print('Invalid input')