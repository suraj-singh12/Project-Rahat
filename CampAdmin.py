from config import config
import datetime     # for current year
import os

from Database import Database

class CampAdmin(Database):
    ''' -------- CampAdmin portal functions -------- '''
    total_person = 0            # this set by __set_class_info(campName)
    new_family_id = 'FLY1000'       # this is invalid, set correctly by __set_class_info(campName)
    usrType = "camp_admin"
    thisYear = str(datetime.datetime.now().year)

    def __set_class_info(self, campName: str):
        # connect to this camp
        cur, conn = self.connect(campName)
        tableName = "main_table" + str(CampAdmin.thisYear)

        # set total no of people in camp
        query = "select count(*) from " + tableName + " where incamp = 'Y';"
        cur.execute(query)
        CampAdmin.total_person = int(cur.fetchone()[0])

        # find max family id
        query = "select max(family_id) from " + tableName + ";"
        cur.execute(query)
        max_id = str(cur.fetchone()[0])

        # set max+1 (new) family ID [available]
        inc = int(max_id[3:])
        inc = inc + 1
        CampAdmin.new_family_id = max_id[0:3] + str(inc)

        cur.close()
        conn.close()


    def __init__(self, identity, pswd):
        self.identity = identity
        if not self.validate(CampAdmin.usrType, self.identity, pswd):
            print("Authentication Failed !")
            exit(-1)
        self.__set_class_info(identity)
    
    def readThis(self, campName:str):
        in_pass = input("Enter your password again: ")

        # read passwords file (this file is on server)
        params = config("passwords.ini","camp_admin")
        ac_pass = params.get(campName)

        # password is not null and matches then proceed to connect 
        if ac_pass is not None and ac_pass == in_pass:
            # connect to camp's database
            cur,conn = self.connect(campName)
            
            relationName = "main_table" + CampAdmin.thisYear 

            os.system("cls")
            # print details of people in camp
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


    def __getInjuryRecords(self, familyId:str, memberNo:int):
        descr = input("Enter Injury Description: ")
        level = input("Enter injury level (Low(L) / Normal(N) / High(H) / Critical(C)): ").upper()
        # print(level)

        while level not in ('L','N','H','C'):
            print("Error, invalid level input. Try again, enter only one character")
            level = input("Enter injury level (Low(L) / Normal(N) / High(H) / Critical(C)): ")

        rec_init = input("Whether recovery initiated? (y/n): ").upper()

        while rec_init not in ('Y','N'):
            print("Error, invalid input. Try again !")
            rec_init = input("Whether recovery initiated? (y/n): ").upper()

        rec_perc = '0'
        if rec_init == 'Y':
            rec_perc = input("Recovery percentage? (0-100): ")
            while int(rec_perc) < 0 or int(rec_perc) > 100:
                print("Error, invalid percentage. Enter percentage from [0-100]")
                rec_perc = input("Recovery percentage? (0-100): ")

        query_data = "'" + familyId + "', " + str(memberNo) + ", '" + descr + "', '" + level + "', '" + rec_init + "', " + rec_perc
        query = "INSERT INTO injury_table2021 values (" + query_data + ");"
        # print(query)
        return query

    # static variables
    vill_city = ''
    loc_in_vc = ''
    def __readDataForQuery(self, member_no:int):
        os.system("cls")
        print("Enter the below details carefully (member : {}): ".format(member_no))
        
        family_id = CampAdmin.new_family_id
        # member_no already recieved
        name = input("Name: ")

        age = input("Age (in years): ")
        if (not int(age)) or int(age) > 110 or int(age) <= 0:
            print("Error! enter a valid age: ")
            age = input("Age (in years): ")
        
        gender = input("Gender (M/F): ").upper()
        while(gender not in ('M', 'F')):
            print("Error! invalid input, try again.")
            gender = input("Gender (M/F): ").upper()

        # this will be useful later on also while querying the dbase, also it is an important aspect that must be known
        if member_no > 1:
            relation = input("Relation (with member 1)? (Mother/Father/Brother/Sister/Cousin): ").lower()
            while relation not in ("mother", "father", "brother", "sister", "cousin"):
                print("Enter a valid relation !")
                relation = input("Relation? (Self/Mother/Father/Brother/Sister/Cousin): ")
        else:
            # only first member can have relation self, others are related to him somehow but not self
            relation = "self"
            # only family mmeber1 will enter address, for other it is same
            CampAdmin.vill_city = input("Village/City: ")
            CampAdmin.loc_in_vc = input("Location in village/city: ")

        inCamp = input("Person will be in camp? (y/n)").upper()
        if inCamp not in ('Y','N'):
            print("Invalid input, only enter one character (y/n)")
            inCamp = input("Person will be in camp? (y/n)").upper()
        
        joinedOn = 'null'
        leftOn = 'null'
        if inCamp == 'Y':
            todayDate = str(datetime.datetime.now())[0:10]
            joinedOn = todayDate
        
        if inCamp == 'Y':
            injury = input("Is there any injury? (y/n)").upper()
            while injury not in ('Y','N'):
                print("Error! invalid input. Try again.")
                injury = input("Is there any injury? (y/n)").upper()
        else:
            injury = '-'    # this means status unknown (for those who aren't in camp)

        query2 = ''
        if injury == 'Y':
            query2 = self.__getInjuryRecords(family_id, member_no)
        
        # there is a minute difference between queries in if and else        
        if joinedOn != 'null':
            query_data = "'" + family_id + "', " + str(member_no) + ", '" + name + "', " + age + ", '" + \
            gender + "', '" + relation + "', '" +  CampAdmin.vill_city + "', '" + CampAdmin.loc_in_vc + "', '" + inCamp + "', '" + \
            joinedOn + "', " + leftOn + ", '" + injury + "'"
        else:
            query_data = "'" + family_id + "', " + str(member_no) + ", '" + name + "', " + age + ", '" + \
            gender + "', '" + relation + "', '" + CampAdmin.vill_city + "', '" + CampAdmin.loc_in_vc + "', '" + inCamp + "', " + \
            joinedOn + ", " + leftOn + ", '" + injury + "'"

        query = "INSERT INTO main_table2021 values (" + query_data + ");"
        # print(query, query2)
        return query, query2


    def writeInto(self, campName:str): 
        """ Insert a record in database / camp """
        in_pass = input("Enter your password again: ")

        # read passwords file (this file is on server)
        params = config("passwords.ini","camp_admin")
        ac_pass = params.get(campName)

        # password is not null and matches then proceed to connect 
        if ac_pass is not None and ac_pass == in_pass:

            # connect to camp's database
            cur,conn = self.connect(campName)

            os.system("cls")
            members = int(input("Enter the number of members in family: "))
            queries = []
            for member_no in range(1,members+1):
                queries.append(self.__readDataForQuery(member_no))
            # print(queries)

            count = 0
            for query in queries:
                cur.execute(query[0])
                count += 1
                if query[1] != '':
                    cur.execute(query[1])
                    count += 1
            cur.close()
            conn.close()
            print("Total rows affected {}".format(count))

    def updateDetails(self, campName):
    # CampAdmin.total_count += 1 
        pass

    def findVacancies(self):
        ''' find vacancies in other camps, and carry people there after informing the camp admin '''
        district = input("Enter your district: ")

        cur, conn = self.connect("all_camp_details")
        tableName = "campdet" + CampAdmin.thisYear
        query = "select campname, camp_admin, email, phone," +\
            "district, city_or_village, total_camp_capacity from " + tableName +\
            " where capacity_full = 'N' and district = '" + district + "';"
        cur.execute(query)

        campDict = {}
        for details in cur.fetchall():
            campDict[str(details[0])] = [details[1],details[2],details[3],details[4],details[5],details[6]]
        cur.close()
        conn.close()

        rowcount = 0
        for campName in campDict.keys():
            # connect to each db one by one
            cur, conn = self.connect(str(campName))
            # query below table and find total count of people in camp
            tableName = "main_table" + CampAdmin.thisYear
            query_total = "select count(*) from " + tableName + " where incamp = 'Y';"
            cur.execute(query_total)
            rowcount = cur.rowcount
            total = int(cur.fetchone()[0])

            values = campDict[campName]
            # now we have vacancy count in index 5 instead of total_capacity
            values[5] = int(values[5]) - total
            # print(campDict[campName])

            cur.close()
            conn.close()
        
        os.system("cls")
        if rowcount == 0:
                print("------------------------------------------------------------------")
                print("Nothing found for this district (kindly check the spelling once)")
                print("------------------------------------------------------------------")
                return
        else:
            print("--------------------------------------------------------------------------------------------------------------------------")
            header = "campName\t Admin\t Email\t\t\t Phone\t\t District    city_or_village    vacancy"
            print(header)

            # print camp info and vacancies
            for campName in campDict.keys():
                print(campName,end = "\t")
                for itms in campDict[campName]:
                    print(itms, end = "\t")
                print()
            print("--------------------------------------------------------------------------------------------------------------------------")
    

    def requestReadSupply(self):
        pass

    def requestGetSupply(self):
        pass

    def readTodayAll(self):
    # make a table containing all the TodayFound/Added in it (also they'd be added in their camps, that's obvious thing)
        pass

    def feedback(self):
    # for each and everything in detail
        pass

    def checkDonationStatus(self):
        pass
