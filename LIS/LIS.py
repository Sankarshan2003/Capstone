#databse for LIS
import mysql.connector
import os
class LIS:
    def __init__(self):
            try:
                self.mydb = mysql.connector.connect(
                    host = "localhost",
                    user = 'root',
                    password = 'sanky10092003'
                )
                print(self.mydb)
            except Exception as e:
                print(e)
    def disconnect(self):
        self.mydb.close()
    def execQuery(self,query):
        mycursor = self.mydb.cursor()
        mycursor.execute(query)
        myresult = mycursor.fetchall()
        return myresult
