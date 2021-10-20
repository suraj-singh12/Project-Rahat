from config import config

from Database import Database

class CampAdmin(Database):
    ''' -------- CampAdmin portal functions -------- '''
    def readThis(self, campName):
        in_pass = input("Enter your password again: ")

        # read passwords file (this file is on server)
        params = config("passwords.ini","camps")
        ac_pass = params.get(campName)

        # password is not null and matches then proceed to connect 
        if ac_pass is not None and ac_pass == in_pass:
            # connect to camp's database
            cur,conn = self.connect(campName)

            relationName = "main_table"             # supposing main_table exists
            cur.execute("SELECT * from " + relationName + ";")
            if cur.rowcount == 0:
                print("No records found!")
            else:
                for row in cur.fetchall():
                    print(row)
            cur.close()
            conn.close()
        else:
            print("Access denied, invalid password !")


    def writeInto(self, campName):
        pass

    def removeFrom(self, campName):
        pass

    def directFrom(self, campName):
        pass

    def findVacancies(self):
        pass

    def requestReadSupply(self):
        pass

    def requestGetSupply(self):
        pass

    def readTodayAll(self):
        pass

    def feedback(self):
        pass

    def checkDonationStatus(self):
        pass
