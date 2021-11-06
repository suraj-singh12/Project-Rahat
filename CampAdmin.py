from config import config
import datetime  # for current year
import os  # for clearing screen
from Database import Database


class CampAdmin(Database):
    """ -------- CampAdmin portal functions -------- """
    # -------------------------------------------------------------------------------------------------
    total_person = 0  # this set by __set_class_info(campName)
    new_family_id = 'FLY1000'  # this is invalid, set correctly by __set_class_info(campName)
    usrType = "camp_admin"
    thisYear = str(datetime.datetime.now().year)

    # -------------------------------------------------------------------------------------------------
    def __init__(self, identity, pswd):
        self.identity = identity
        if not self.validate(CampAdmin.usrType, self.identity, pswd):
            print("Authentication Failed !")
            exit(-1)
        self.__set_class_info(identity)

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

    # -------------------------------------------------------------------------------------------------

    def readThis(self, campName: str):
        in_pass = input("Enter your password again: ")

        # read passwords file (this file is on server)
        params = config("passwords.ini", "camp_admin")
        ac_pass = params.get(campName)

        # password is not null and matches then proceed to connect 
        if ac_pass is not None and ac_pass == in_pass:
            # connect to camp's database
            cur, conn = self.connect(campName)

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

    # -------------------------------------------------------------------------------------------------

    @staticmethod
    def __getInjuryRecords(familyId: str, memberNo: int):
        descr = input("Enter Injury Description: ")
        level = input("Enter injury level (Low(L) / Normal(N) / High(H) / Critical(C)): ").upper()
        # print(level)

        while level not in ('L', 'N', 'H', 'C'):
            print("Error, invalid level input. Try again, enter only one character")
            level = input("Enter injury level (Low(L) / Normal(N) / High(H) / Critical(C)): ")

        rec_init = input("Whether recovery initiated? (y/n): ").upper()

        while rec_init not in ('Y', 'N'):
            print("Error, invalid input. Try again !")
            rec_init = input("Whether recovery initiated? (y/n): ").upper()

        rec_perc = '0'
        if rec_init == 'Y':
            rec_perc = input("Recovery percentage? (0-100): ")
            while int(rec_perc) < 0 or int(rec_perc) > 100:
                print("Error, invalid percentage. Enter percentage from [0-100]")
                rec_perc = input("Recovery percentage? (0-100): ")

        query_data = "'" + familyId + "', " + str(
            memberNo) + ", '" + descr + "', '" + level + "', '" + rec_init + "', " + rec_perc
        query = "INSERT INTO injury_table2021 values (" + query_data + ");"
        # print(query)
        return query

    # -------------------------------------------------------------------------------------------------

    # static variables
    vill_city = ''
    loc_in_vc = ''

    def __readDataForQuery(self, member_no: int):
        os.system("cls")
        print("Enter the below details carefully (member : {}): ".format(member_no))

        family_id = CampAdmin.new_family_id
        # member_no already received
        name = input("Name: ")

        age = input("Age (in years): ")
        if (not int(age)) or int(age) > 110 or int(age) <= 0:
            print("Error! enter a valid age: ")
            age = input("Age (in years): ")

        gender = input("Gender (M/F): ").upper()
        while gender not in ('M', 'F'):
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
            # only family member1 will enter address, for other it is same
            CampAdmin.vill_city = input("Village/City: ")
            CampAdmin.loc_in_vc = input("Location in village/city: ")

        inCamp = input("Person will be in camp? (y/n)").upper()
        if inCamp not in ('Y', 'N'):
            print("Invalid input, only enter one character (y/n)")
            inCamp = input("Person will be in camp? (y/n)").upper()

        joinedOn = 'null'
        leftOn = 'null'
        if inCamp == 'Y':
            todayDate = str(datetime.datetime.now())[0:10]
            joinedOn = todayDate

        if inCamp == 'Y':
            injury = input("Is there any injury? (y/n)").upper()
            while injury not in ('Y', 'N'):
                print("Error! invalid input. Try again.")
                injury = input("Is there any injury? (y/n)").upper()
        else:
            injury = '-'  # this means status unknown (for those who aren't in camp)

        query2 = ''
        if injury == 'Y':
            query2 = self.__getInjuryRecords(family_id, member_no)

        # there is a minute difference between queries in if and else        
        if joinedOn != 'null':
            query_data = "'" + family_id + "', " + str(member_no) + ", '" + name + "', " + age + ", '" + \
                         gender + "', '" + relation + "', '" + CampAdmin.vill_city + "', '" + CampAdmin.loc_in_vc + \
                         "', '" + inCamp + "', '" + joinedOn + "', " + leftOn + ", '" + injury + "'"
        else:
            query_data = "'" + family_id + "', " + str(member_no) + ", '" + name + "', " + age + ", '" + \
                         gender + "', '" + relation + "', '" + CampAdmin.vill_city + "', '" + CampAdmin.loc_in_vc + \
                         "', '" + inCamp + "', " + joinedOn + ", " + leftOn + ", '" + injury + "'"

        query = "INSERT INTO main_table2021 values (" + query_data + ");"
        # print(query, query2)
        return query, query2

    # -------------------------------------------------------------------------------------------------

    def writeInto(self, campName: str):
        """ Insert a record in database / camp """
        in_pass = input("Enter your password again: ")

        # read passwords file (this file is on server)
        params = config("passwords.ini", "camp_admin")
        ac_pass = params.get(campName)

        # password is not null and matches then proceed to connect 
        if ac_pass is not None and ac_pass == in_pass:

            # connect to camp's database
            cur, conn = self.connect(campName)

            os.system("cls")
            members = int(input("Enter the number of members in family: "))
            queries = []
            for member_no in range(1, members + 1):
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

    # -------------------------------------------------------------------------------------------------

    def updateDetails(self, campName):
        pass

    # -------------------------------------------------------------------------------------------------

    def findVacancies(self):
        """ find vacancies in other camps, and carry people there after informing the camp admin """
        district = input("Enter your district: ")

        cur, conn = self.connect("all_camp_details")
        tableName = "campdet" + CampAdmin.thisYear
        query = "select campname, camp_admin, email, phone," + \
                "district, city_or_village, total_camp_capacity from " + tableName + \
                " where capacity_full = 'N' and district = '" + district + "';"
        cur.execute(query)

        campDict = {}
        for details in cur.fetchall():
            campDict[str(details[0])] = [details[1], details[2], details[3], details[4], details[5], details[6]]
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
            print(
                '''--------------------------------------------------
                ------------------------------------------------------------------------''')
            header = "campName\t Admin\t Email\t\t\t Phone\t\t District    city_or_village    vacancy"
            print(header)

            # print camp info and vacancies
            for campName in campDict.keys():
                print(campName, end="\t")
                for itms in campDict[campName]:
                    print(itms, end="\t")
                print()
            print(
                '''--------------------------------------------------
                                ------------------------------------------------------------------------''')

    # -------------------------------------------------------------------------------------------------

    def readItemAvailability(self):
        """ find if an item is available in any camp [in a given district] """
        item = input("Enter item name: ")
        itm_type = input("Enter item type (regular(r)/medical(m)): ")
        while itm_type not in ('r', 'm'):
            print("Error, invalid input! ")
            itm_type = input("Enter item type (regular(r)/medical(m)): ")

        district = input("Enter district: ")
        # set item type accordingly
        if itm_type == 'r':
            itm_type = "regular"
        else:
            itm_type = "medical"

        # get a list of all databases (camps, other default db)
        db_list = self.listAllDatabases()

        os.system("cls")
        # print relevant header
        if itm_type == "medical":
            header = "(campName, district, city_or_village, item_name, item_type, description, age_groups, qty)\n"
        else:
            header = "(campName, district, city_or_village, item_name, item_type, description, qty)\n"
        print(header)

        availCampList = list()
        for campName in db_list:
            if campName[0:4] == 'camp':  # if it is a camp only then proceed
                cur, conn = self.connect(str(campName))
                # initial check to ensure camp is from same district
                checkQuery = "select district, city_or_village from my_camp_info where district ilike '" + \
                             district + "' and year = '" + CampAdmin.thisYear + "';"
                cur.execute(checkQuery)
                # print(cur.fetchall())

                if cur.rowcount == 0:
                    cur.close()
                    conn.close()
                    continue
                else:
                    availCampList.append(campName)
                    city_or_vill = str(cur.fetchall()[0][1])
                    tableName = itm_type + "_supply_table" + CampAdmin.thisYear

                    # query to find the item
                    query = "select * from " + tableName + " where item_name ilike '%" + item + "%';"
                    cur.execute(query)

                    # if query result is not empty
                    if cur.rowcount > 0:
                        # fetch all output rows
                        for row in cur.fetchall():
                            # add camp name at starting, followed by district, cityName
                            row = list(row)
                            row.insert(0, campName)
                            row.insert(1, district)
                            row.insert(2, city_or_vill)
                            row = tuple(row)
                            # print the updated row
                            print(row)
                        print()

        return availCampList

    # -------------------------------------------------------------------------------------------------

    def contactSupplyFromCamps(self):
        """ get the contact of admins of camps who have certain item available """
        availCampList = self.readItemAvailability()
        if len(availCampList) > 0:
            campName = input("Enter the campName from above list of camps: ")
            while campName not in availCampList and campName != '0':
                print("Error, the entered camp is not in list.")
                print("Try again or press 0 to exit..")
                campName = input("Enter the campName from above list of camps: ")

            # find current year admin's info
            query = "select campid, camp_admin, mobile, email from my_camp_info where year = '" \
                    + CampAdmin.thisYear + "';"
            header = "(CampId      campAdmin     Mobile         Email)"
            print(header)

            cur, conn = self.connect(campName)
            cur.execute(query)
            adminData = cur.fetchall()[0]
            print(adminData)
            cur.close()
            conn.close()
        else:
            print("No camp in the entered district has the item you are searching for !")
            print("Kindly Try after some time or try other district")

    # -------------------------------------------------------------------------------------------------

    def readTodayAll(self):
        """ read all the entries of today in all camps """

        os.system("cls")
        allCamps = self.listAllDatabases()

        for camp in allCamps:
            if camp[0:4] == 'camp':
                cur, conn = self.connect(camp)
                query = "select * from today_all;"
                cur.execute(query)

                header = "(Family_ID, Member_No, Name, Age, Gender, Relation, Village\\City, location, inCamp)\n"
                print(header)
                for row in cur.fetchall():
                    print(row)
        print()

    # -------------------------------------------------------------------------------------------------
    def requestSupplyFromMain(self, campName):
        """ send supply request to govt(sysAdmin) team """

        campId = campName[4:]
        # get item details
        itmName = input("Enter item name: ")
        while len(itmName) < 2:
            print("Enter a valid item name !!")
            itmName = input("Enter item name: ")

        itmType = input("Enter item type (regular(r)/medical(m)): ")
        while itmType not in ('r', 'm'):
            print("Error, try again. Enter only single character (r,m)")
            itmType = input("Enter item type (regular(r)/medical(m)): ")

        if itmType == 'r':
            itmType = "regular"
        else:
            itmType = "medical"

        itmDescription = input("Enter item description: ")
        qty = input("Enter quanity of item required: ")

        # demand table
        tableName = "demand" + CampAdmin.thisYear
        # query to insert the demanded item in demand table
        query = "insert into " + tableName + " values('" + campId + "', '" + \
                itmName + "', '" + itmType + "', '" + itmDescription + "', " + qty + ");"
        # connect to all camp database (common/general database)
        cur, conn = self.connect("all_camp_details")
        cur.execute(query)  # make the demand (insert the demand in table)

        if cur.rowcount == 1:
            print("Request Successfully submitted.")
        else:
            print("There was an ERROR in submission of report !!")
            print("Try again...")
        print()

        cur.close()
        conn.close()

    # -------------------------------------------------------------------------------------------------

    def updateSupplyData(self, campName: str):
        """ add/update the supply records in camp """
        os.system("cls")
        # menu
        print("1. Add a new item in records")
        print("2. Update an already existing item")
        print("0 to exit.")
        wantTO = int(input("Choice: "))

        if wantTO > 2 or wantTO < 1:
            os.system("cls")
            return

        # get and set category correctly
        category = input("Enter supply type (regular(r)/medical(m)): ")
        while category not in ('r', 'm'):
            print("Error, wrong choice! Enter only one character (r/m)")
            category = input("Enter supply type (regular(r)/medical(m)): ")
        if category == 'r':
            category = "regular"
        else:
            category = "medical"
        # set tablename
        tableName = category + "_supply_table" + CampAdmin.thisYear

        # if want to add new item
        if wantTO == 1:
            # get item details
            itemName = input("Enter the name of item: ").lower()
            while len(itemName) < 2:
                itemName = input("Enter the name of item: ")

            itemType = input("Enter the type of item: ")
            while itemType == '':
                itemType = input("Enter the type of item: ")

            itemDescription = input("Enter item description: ")
            while len(itemDescription) < 2:
                print("Enter a valid item description")
                itemDescription = input("Enter item description: ")

            quantity = input("Enter quantity: ")
            while not quantity.isdigit():
                print("Enter valid quantity (numeric)")
                quantity = input("Enter quantity: ")
            while int(quantity) < 0:
                print("Error, quantity can't be in negative !! Try again...")
                quantity = input("Enter quantity: ")

            ageGroups = ''
            if category == "medical":
                ageGroups = input("Which age groups it is applicable to (all/6-10/etc): ")

            # query created according to category
            if category == "medical":
                query = "insert into " + tableName + " values('" + itemName + "', '" + \
                        itemType + "', '" + itemDescription + "', '" + ageGroups + "', " + quantity + ");"
            else:
                query = "insert into " + tableName + " values('" + itemName + "', '" + \
                        itemType + "', '" + itemDescription + "', " + quantity + ");"
            # connect to camp database & execute query
            cur, conn = self.connect(campName)
            cur.execute(query)
            print()

            if cur.rowcount == 1:
                print("Successfully added record")
            else:
                print("There was an ERROR in adding the record !! Try again.")
            cur.close()
            conn.close()

        else:
            cur, conn = self.connect(campName)

            # first get all supply item names
            query = "select item_name from " + tableName + ";"
            cur.execute(query)
            # print item names
            allItems = cur.fetchall()
            listOfItems = list()
            for itm in allItems:
                listOfItems.append(itm[0])
            print(listOfItems)

            itemName = input("\nEnter the itemName to update it's supply: ").lower()

            # if the name is not in supply item list
            while itemName not in listOfItems:
                print("Error, item does not exists in pre existing items!! Try again...")
                itemName = input("\nEnter the itemName to update it's supply: ").lower()
            qty = input("Enter updated quantity: ")

            # create and execute the query 
            query = "update " + tableName + " set qty = " + qty + " where item_name = '" + itemName + "';"
            cur.execute(query)
            print()

            if cur.rowcount == 1:
                print("Successfully updated record")
            else:
                print("There was an ERROR in updating the record !! Try again.")
            cur.close()
            conn.close()

    # -------------------------------------------------------------------------------------------------

    def feedback(self, campName):
        # for each and everything in detail
        feedback = input("Enter feedback below\n")
        cur, conn = self.connect("all_camp_details")
        campid = campName[4:]

        feedbackTable = "feedback" + CampAdmin.thisYear
        query = "select campid from " + feedbackTable + ";"
        cur.execute(query)
        campNames = cur.fetchall()[0]
        # print(campNames)
        if campid not in campNames:
            query = "insert into " + feedbackTable + " values('" + campid + "','" + feedback + "');"
            cur.execute(query)
        else:
            query = "update " + feedbackTable + " set feedback = '" + feedback + "' where campid = '" + campid + "';"
            cur.execute(query)

        if cur.rowcount == 1:
            print("\nFeedback successfully submitted.\n")
        else:
            print("\nError, could not submit feedback.\n")
        cur.close()
        conn.close()

# -------------------------------------------------------------------------------------------------
