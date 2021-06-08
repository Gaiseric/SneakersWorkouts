import csv
import pandas as pd
import sqlite3 as sql

class DBManager:
    
    def __init__(self, dbname: str):
        self.__dbname = dbname
        self.__con = None
        self.__cur = None

    def set_connection(self):
        self.__con = sql.connect(self.__dbname)
        self.__cur = self.__con.cursor()

    def close_connection(self):
        self.__con.close()

    def create_new_sneaker(self, sneakername):
        try:
            str = "CREATE TABLE " + sneakername + " (Date text, Type text, Distance real)"
            self.__cur.execute(str)
            self.__con.commit()
            return 'Sneaker added to DB'
        except Exception as e:
            return e

    def create_new_workout(self, sneakername, values):
        tmp = (values[0], values[1])
        try:
            str = "SELECT Date, Type FROM " + sneakername
            self.__cur.execute(str)
            for row in self.__cur:
                if tmp == row:
                    raise Exception('Such workout already exists')
            str = "INSERT INTO " + sneakername + " VALUES (?,?,?)"
            self.__cur.execute(str, values)
            self.__con.commit()
            return 'New workout added successfull'
        except Exception as e:
            return e

    def add_workouts_from_csv(self, sneakername, filename):
        workouts_list = []
        try:
            with open(filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    workouts_list.append(tuple((row['Date'], row['Type'], row['Distance'])))
            str = "INSERT INTO " + sneakername + " VALUES (?, ?, ?)"
            self.__cur.executemany(str, workouts_list)
            self.__con.commit()
            return 'Workouts from CSV file added successfull'
        except Exception as e:
            return e
    
    def add_workouts_to_csv(self, sneakername, filename):
        try:   
            str = "SELECT * FROM " + sneakername
            df = pd.read_sql(str, self.__con)
            df.to_csv(filename, index=False)
            return 'File saved successfull'
        except Exception as e:
            return e

    def add_workouts_to_xlsx(self, sneakername, filename):
        try:   
            str = "SELECT * FROM " + sneakername
            df = pd.read_sql(str, self.__con)
            df.to_excel(filename, index=False)
            return 'File saved successfull'
        except Exception as e:
            return e

    def delete_sneaker(self, sneakername):
        try:
            str = "DROP TABLE " + sneakername
            self.__cur.execute(str)
            self.__con.commit()
            return 'Sneaker and his workouts deleted successfull'
        except Exception as e:
            return e        

    def edit_workout(self, sneakername, values):
        tmp = (values[0], values[1])
        try:
            str = "SELECT Date, Type FROM " + sneakername
            self.__cur.execute(str)
            cnt = False
            for row in self.__cur:
                if tmp == row:
                    cnt = True
            if cnt == False:
                raise Exception('No such workout')
            str = "UPDATE " + sneakername + " SET Distance=? WHERE Date=? AND Type=?"
            data = (values[2], values[0], values[1])
            self.__cur.execute(str, data)
            self.__con.commit()
            return 'Workout updated successfull'
        except Exception as e:
            return e

    def delete_workout(self, sneakername, values):
        tmp = (values[0], values[1])
        try:
            str = "SELECT Date, Type FROM " + sneakername
            self.__cur.execute(str)
            cnt = False
            for row in self.__cur:
                if tmp == row:
                    cnt = True
            if cnt == False:
                raise Exception('No such workout')
            str = "DELETE FROM " + sneakername + " WHERE Date=? AND Type=? AND Distance=?"
            self.__cur.execute(str, values)
            self.__con.commit()
            return 'Workout deleted successfull'
        except Exception as e:
            return e    

    def print_workouts_for_sneaker(self, sneakername):
        try: 
            str = "SELECT * FROM " + sneakername
            df = pd.read_sql(str, self.__con)
            return df
        except Exception as e:
            return e

    def print_sneakers_names(self):
        try:
            str = "SELECT name FROM sqlite_master WHERE type='table'"
            res = self.__con.execute(str)
            lst = []
            for name in res:
                lst.append(name)
            return lst
        except Exception as e:
            return e