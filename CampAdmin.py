from config import config
import datetime  # for current year
import os  # for clearing screen
from Database import Database
from PyQt5 import QtWidgets
import SelectTableToRead_UI
import MainTable2021_UI
import NewPersonForm_UI


class NewPerson(QtWidgets.QWidget, NewPersonForm_UI.Ui_Dialog):
    def __init__(self):
        super(NewPerson, self).__init__()
        self.setupUi(self)
        # disable injury subform (input fields)
        self.lineEdit_7.setEnabled(False)
        self.comboBox.setEnabled(False)
        self.comboBox_2.setEnabled(False)
        self.spinBox_2.setEnabled(False)
        # disable injury subform (labels)
        self.label_9.setEnabled(False)
        self.label_10.setEnabled(False)
        self.label_11.setEnabled(False)
        self.label_12.setEnabled(False)
        self.label_14.setEnabled(False)


class SelectATable(QtWidgets.QWidget, SelectTableToRead_UI.Ui_Dialog):
    def __init__(self):
        super(SelectATable, self).__init__()
        self.setupUi(self)


class MainTable(QtWidgets.QMainWindow, MainTable2021_UI.Ui_MainWindow):
    def __init__(self):
        super(MainTable, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()

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
        # connect to camp's database
        cur, conn = self.connect(campName)

        mainTable = "main_table" + CampAdmin.thisYear
        injuryTable = "injury_table" + CampAdmin.thisYear

        os.system("cls")
        cur.execute("SELECT * from " + mainTable + ";")
        mainTableRows = cur.fetchall()
        cur.execute("SELECT * from " + injuryTable + ";")
        injuryTableRows = cur.fetchall()

        # print details of people in camp
        if cur.rowcount == 0:
            print("No records found!")
        else:
            total_length = len(mainTableRows)
            length1 = 0
            length2 = 0

            while length1 < total_length:
                print("------------------------"*5)
                print("BASIC  details: ", end='')
                print(mainTableRows[length1])
                if mainTableRows[length1][8] == 'Y':
                    print("INJURY details: ", end='')
                    print(injuryTableRows[length2])
                    length2 += 1
                length1 += 1
                print("------------------------"*5)
                print()
        cur.close()
        conn.close()

    # -------------------------------------------------------------------------------------------------

    @staticmethod
    def __getInjuryRecords(familyId: str, memberNo: int, data_ith1: tuple):
        descr = data_ith1[0]
        level = ''
        if data_ith1[1] == 'Low':
            level = 'L'
        elif data_ith1[1] == 'Normal':
            level = 'N'
        elif data_ith1[1] == 'High':
            level = 'H'
        else:
            level = 'C'
        # print(level)

        rec_init = ''
        if data_ith1[2] == 'Yes':
            rec_init = 'Y'
        else:
            rec_init = 'N'

        rec_perc = '0'
        if rec_init == 'Y':
            rec_perc = data_ith1[3]

        query_data = "'" + familyId + "', " + str(
            memberNo) + ", '" + descr + "', '" + level + "', '" + rec_init + "', " + rec_perc
        query = "INSERT INTO injury_table2021 values (" + query_data + ");"
        # print(query)
        return query

    # -------------------------------------------------------------------------------------------------

    # static variables
    vill_city = ''
    loc_in_vc = ''

    def __readDataForQuery(self, member_no: int, data_ith: tuple):
        # os.system("cls")
        print("Enter the below details carefully (member : {}): ".format(member_no))
        print(data_ith)

        family_id = CampAdmin.new_family_id
        # member_no already received
        name = data_ith[0][0]

        age = data_ith[0][1]

        gender = data_ith[0][2]

        relation = data_ith[0][3].lower()
        if member_no == 1:
            # only family member1 will enter address, for other it is same
            CampAdmin.vill_city = data_ith[0][4]
            CampAdmin.loc_in_vc = data_ith[0][5]

        inCamp = data_ith[0][7].upper()

        joinedOn = 'null'
        leftOn = 'null'
        if inCamp == 'Y':
            todayDate = str(datetime.datetime.now())[0:10]
            joinedOn = todayDate

            injury = data_ith[0][8].upper()
        else:
            injury = '-'  # this means status unknown (for those who aren't in camp)

        query2 = ''
        if injury == 'Y':
            query2 = self.__getInjuryRecords(family_id, member_no, data_ith[1])

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

    def writeInto(self, campName: str, data: tuple):
        """ Insert a record in database / camp """

        # connect to camp's database
        cur, conn = self.connect(campName)

        # os.system("cls")
        members = len(data)
        queries = []
        for member_no in range(1, members + 1):
            queries.append(self.__readDataForQuery(member_no, data[member_no-1]))
        print(queries)

        count = 0
        for query in queries:
            cur.execute(query[0])
            count += 1
            if query[1] != '':
                cur.execute(query[1])
                count += 1
        cur.close()
        conn.close()
        print("Total rows affected {}\n".format(count))

        print("Provide below familyId card to the person1 of family")
        print("---------------"*5)
        print("FamilyID: " + CampAdmin.new_family_id)
        print("---------------" * 5)
        message = "Provide Family Id card to the Person1 of family" + \
                  "\n\n With ID - Family ID: " + CampAdmin.new_family_id + "\t\t"
        return message

    # -------------------------------------------------------------------------------------------------

    def updateDetails(self, campName):
        """ update details of a person """

        # connect to camp's database
        cur, conn = self.connect(campName)
        os.system("cls")

        # ------------------- Menu -------------------
        print("1. Update injury status of person in camp")
        print("2. Update leftOn date for a person who is leaving the camp")
        cat = input("Which category to update?(1/2) ")
        while cat not in ('1', '2'):
            print("\n\nEnter a valid choice")
            cat = input("Which category to update?(1/2) ")
        # ------------------- ------------------- -----

        # get basic input to identify the person
        familyId = input("\nEnter family ID: ")
        while familyId == '':
            familyId = input("\nEnter family ID: ")
        memberNo = input("Enter member no: ")
        while memberNo == '':
            memberNo = input("Enter member no: ")
        # table names
        mainTable = "main_table" + CampAdmin.thisYear
        injuryTable = "injury_table" + CampAdmin.thisYear

        # ------------------- Menu functions -------------------
        if cat == '1':
            # first find whether the person recognised by (familyId, memberNo) is having injury or not
            query = "select name from " + mainTable + \
                    " where family_id='" + familyId + "' and member_no=" + memberNo + \
                    " and injury='Y';"
            cur.execute(query)

            # if no injury then return
            if cur.rowcount == 0:
                print("Error!, can't set level as injury is set to NO for the person.")
                return

            # if injury is there, then print the person name
            os.system("cls")
            print("Found this record -\n")
            for row in cur.fetchall():
                print(row)
            print()

            # ------------------- get injury details -------------------
            print("Injury levels: Low(L), Normal(N), High(H), Critical(C)")
            injuryLevel = input("Enter injury level: (L/N/H/C): ").upper()
            while injuryLevel not in ('L', 'N', 'H', 'C'):
                print("Incorrect input, try again!")
                injuryLevel = input("Enter injury level: (L/N/H/C): ").upper()

            recoveryPercentage = input("Enter recovery percentage: ")
            while (not recoveryPercentage.isdigit()) or int(recoveryPercentage) > 100 or int(recoveryPercentage) < 0:
                print("Invalid input, Enter a value in [0,100] range")
                recoveryPercentage = input("Enter recovery percentage: ")
            # ------------------- ------------------- -------------------

            # update the database with new details
            query = "update " + injuryTable + \
                " set injury_level='" + injuryLevel + "', " + \
                "recovery_initiated='Y', recovery_percent=" + recoveryPercentage + " " + \
                "where family_id='" + familyId + "' and member_no=" + memberNo + ";"

            cur.execute(query)
            print("Total rows affected: {}".format(cur.rowcount))
            # ------------------- END -------------------

        # ------------------- if the cat = '2' (i.e. choice category = 2) -------------------
        else:
            query = "select name, joinedon, lefton from " + mainTable + " where family_id='" + familyId + \
                "' and member_no=" + memberNo + " and joinedon is not null and lefton is null;"
            cur.execute(query)

            # if no record found then return
            if cur.rowcount == 0:
                print("Error! The person is either not in camp or has already left")
                print("Exiting...")
                return

            # else proceed
            print("Matching records: ")
            for row in cur.fetchall():
                print(row)

            consent = input("Proceed?(y/n) ").lower()

            if consent == 'y':
                # get today's date
                leavingDate = str(datetime.datetime.now())[0:10]

                updateQuery = "update " + mainTable + " set lefton ='" + leavingDate + "'" + \
                    " where family_id='" + familyId + "' and member_no=" + memberNo + ";"
                cur.execute(updateQuery)

                if cur.rowcount == 1:
                    print("Success !")
                else:
                    print("An error occurred! please try again")

    # -------------------------------------------------------------------------------------------------

    def findVacancies(self):
        """ find vacancies in other camps, and carry people there after informing the camp admin """
        district = input("Enter your district: ")

        cur, conn = self.connect("all_camp_details")
        tableName = "campdet" + CampAdmin.thisYear
        query = "select camp_id, camp_admin, email, phone," + \
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
            query = "select camp_id, camp_admin, mobile, email from my_camp_info where year = '" \
                    + CampAdmin.thisYear + "';"
            header = "(Camp_id      campAdmin     Mobile         Email)"
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
        query = "select camp_id from " + feedbackTable + ";"
        cur.execute(query)
        campNames = cur.fetchall()[0]
        # print(campNames)
        if campid not in campNames:
            query = "insert into " + feedbackTable + " values('" + campid + "','" + feedback + "');"
            cur.execute(query)
        else:
            query = "update " + feedbackTable + " set feedback = '" + feedback + "' where camp_id = '" + campid + "';"
            cur.execute(query)

        if cur.rowcount == 1:
            print("\nFeedback successfully submitted.\n")
        else:
            print("\nError, could not submit feedback.\n")
        cur.close()
        conn.close()

# -------------------------------------------------------------------------------------------------
