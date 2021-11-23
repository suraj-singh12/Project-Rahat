from config import config
import datetime  # for current year
import os  # for clearing screen
from Database import Database
from PyQt5 import QtWidgets
import SelectTableToRead_UI
import MainTable2021_UI
import NewPersonForm_UI
import UpdateDetailsPerson_UI
import WhichResource_UI
import RegularResourceAvailibility_UI
import MedicalResourceAvailibility_UI
import RequestSupply_UI
import UpdateSupplyData_UI
import VacanciesInCamps_UI


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


class RequestSupply(QtWidgets.QWidget, RequestSupply_UI.Ui_RequestSupplyPopup):
    def __init__(self):
        super(RequestSupply, self).__init__()
        self.setupUi(self)
        # self.submit_pushButton.setFocus()
        self.pushButton_submit.setAutoDefault(True)
        self.pushButton_reset.setAutoDefault(True)
        self.pushButton_reset.clicked.connect(self.reset)

    def reset(self):
        self.lineEdit_item_name.clear()
        self.lineEdit_item_desc.clear()
        self.comboBox_item_type.setCurrentIndex(0)
        self.spinbox_quantity.setValue(0)


class VacanciesInCamp(QtWidgets.QWidget, VacanciesInCamps_UI.Ui_Dialog):
    def __init__(self):
        super(VacanciesInCamp, self).__init__()
        self.setupUi(self)
        self.pushButton_ok.setFocus()
        self.pushButton_ok.setAutoDefault(True)
        self.pushButton_ok.clicked.connect(self.ok_pressed)

    def ok_pressed(self):
        # close the window
        self.close()


class UpdateSupply(QtWidgets.QWidget, UpdateSupplyData_UI.Ui_UpdateSupplyDataPopup):
    def __init__(self):
        super(UpdateSupply, self).__init__()
        self.setupUi(self)
        self.lineEdit_item_name.setFocus()
        self.pushButton_reset.setAutoDefault(True)
        self.pushButton_submit.setAutoDefault(True)
        self.pushButton_reset.clicked.connect(self.reset)

        self.label_age_groups.setEnabled(False)
        self.comboBox_age_group.setEnabled(False)
        self.label_item_type.setEnabled(False)
        self.lineEdit_item_type.setEnabled(False)
        self.comboBox_category.currentIndexChanged.connect(self.toggle_age_itm_type)

    def toggle_age_itm_type(self):
        if self.comboBox_category.currentText().lower() == 'medical':
            self.label_age_groups.setEnabled(True)
            self.comboBox_age_group.setEnabled(True)
            self.label_item_type.setEnabled(True)
            self.lineEdit_item_type.setEnabled(True)
        else:
            self.label_age_groups.setEnabled(False)
            self.comboBox_age_group.setEnabled(False)
            self.comboBox_age_group.setCurrentIndex(0)
            self.label_item_type.setEnabled(False)
            self.lineEdit_item_type.setEnabled(False)
            self.lineEdit_item_type.clear()

    def reset(self):
        self.lineEdit_item_name.clear()
        self.comboBox_category.setCurrentIndex(0)
        self.comboBox_age_group.setCurrentIndex(0)
        self.lineEdit_item_type.clear()
        self.lineEdit_item_description.clear()
        self.lineEdit_item_description.clear()
        self.spinBox_quantity.setValue(0)


class UpdatePerson(QtWidgets.QWidget, UpdateDetailsPerson_UI.Ui_Dialog):
    def __init__(self):
        super(UpdatePerson, self).__init__()
        self.setupUi(self)


class ResourceType(QtWidgets.QWidget, WhichResource_UI.Ui_Dialog):
    def __init__(self):
        super(ResourceType, self).__init__()
        self.setupUi(self)


class MedicalResource(QtWidgets.QWidget, MedicalResourceAvailibility_UI.Ui_Dialog):
    def __init__(self):
        super(MedicalResource, self).__init__()
        self.setupUi(self)
        self.pushButton.setFocus()
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class RegularResource(QtWidgets.QWidget, RegularResourceAvailibility_UI.Ui_Dialog):
    def __init__(self):
        super(RegularResource, self).__init__()
        self.setupUi(self)
        self.pushButton.setFocus()
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


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
        # print("here")
        if not self.validate(CampAdmin.usrType, self.identity, pswd):
            print("Authentication Failed !")
            exit(-1)
        # print("semi-safe")
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
        # print("safe till here")

        max_id = str(cur.fetchone()[0])
        if max_id is not None:
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

    def updateDetails(self, campName, data: tuple):
        """ update details of a person """
        message = ''
        print("Inside UpdateDetails")
        # connect to camp's database
        cur, conn = self.connect(campName)
        # os.system("cls")

        # # ------------------- Menu -------------------
        # print("1. Update injury status of person in camp")
        # print("2. Update leftOn date for a person who is leaving the camp")
        # cat = input("Which category to update?(1/2) ")
        # while cat not in ('1', '2'):
        #     print("\n\nEnter a valid choice")
        #     cat = input("Which category to update?(1/2) ")
        # ------------------- ------------------- -----

        # get basic input to identify the person
        familyId = data[0]
        memberNo = data[1]
        # table names
        mainTable = "main_table" + CampAdmin.thisYear
        injuryTable = "injury_table" + CampAdmin.thisYear

        # ------------------- Menu functions -------------------
        if data[2] != '-':      # that means person has some injury
            # first find whether the person recognised by (familyId, memberNo) is having injury or not
            query = "select name from " + mainTable + \
                    " where family_id='" + familyId + "' and member_no=" + memberNo + \
                    " and injury='Y';"
            cur.execute(query)

            # if no injury then return
            if cur.rowcount == 0:
                print("Error!, can't set level as injury is set to NO for the person.")
                message += "couldn't set injury level as injury is set to NO for the person.\n"
            else:
                # if injury is there, then print the person name
                # os.system("cls")
                # print("Found this record -\n")
                # for row in cur.fetchall():
                #     print(row)
                # print()
                # ------------------- get injury details -------------------
                print("Injury levels: Low(L), Normal(N), High(H), Critical(C)")
                injuryLevel = data[2]
                recoveryPercentage = data[3]
                # ------------------- ------------------- -------------------

                # update the database with new details
                query = "update " + injuryTable + \
                    " set injury_level='" + injuryLevel + "', " + \
                    "recovery_initiated='Y', recovery_percent=" + recoveryPercentage + " " + \
                    "where family_id='" + familyId + "' and member_no=" + memberNo + ";"

                cur.execute(query)
                print("Total rows affected: {}".format(cur.rowcount))
                message += 'Injury records updated\n'
                # ------------------- END -------------------

        if data[4] == 'Y':      # means Leaving Today is checked
            query = "select name, joinedon, lefton from " + mainTable + " where family_id='" + familyId + \
                "' and member_no=" + memberNo + " and joinedon is not null and lefton is null;"
            cur.execute(query)

            # if no record found then return
            if cur.rowcount == 0:
                print("Error! The person is either not in camp or has already left")
                print("Exiting...")
                # override message with error message
                message = 'Error! Person not in Camp!!\t\t'
                return message

            # else proceed
            print("Matching records: ")
            for row in cur.fetchall():
                print(row)

            # get today's date
            leavingDate = str(datetime.datetime.now())[0:10]

            updateQuery = "update " + mainTable + " set lefton ='" + leavingDate + "'" + \
                " where family_id='" + familyId + "' and member_no=" + memberNo + ";"
            cur.execute(updateQuery)

            if cur.rowcount == 1:
                print("Success !")
                message += '\nleaving Date successfully updated!\n Person leaves Today.'
            else:
                print("An error occurred! please try again")
                message += 'Could not update leaving date!!'
        return message

    # -------------------------------------------------------------------------------------------------

    def findVacancies(self, district):
        """ find vacancies in other camps, and carry people there after informing the camp admin """
        # district = input("Enter your district: ")
        print("reached target")

        cur, conn = self.connect("all_camp_details")

        # find all the databases which are not full
        tableName = "campdet" + CampAdmin.thisYear
        query = "select camp_name, camp_admin, email, mobile," + \
                "district, city_or_village, total_camp_capacity from " + tableName + \
                " where capacity_full = 'N' and district ilike '" + district + "';"
        cur.execute(query)

        campDict = {}
        for details in cur.fetchall():
            campDict[str(details[0])] = [details[1], details[2], details[3], details[4], details[5], details[6]]
        cur.close()
        conn.close()
        print(campDict)

        rowcount = 0
        # in each camp find total no of people who are in camp, so total vacancies can be found for each camp
        for campName in campDict.keys():
            # connect to each db one by one
            cur, conn = self.connect(str(campName))
            # query below table and find total count of people in camp
            tableName = "main_table" + CampAdmin.thisYear
            query_total = "select count(*) from " + tableName + " where incamp = 'Y';"
            cur.execute(query_total)

            rowcount = cur.rowcount
            total_in = int(cur.fetchone()[0])

            values = campDict[campName]
            # now we have vacancy count in index 5 instead of total_capacity
            values[5] = int(values[5]) - total_in
            # print(campDict[campName])
            cur.close()
            conn.close()

        final_list  = []
        for campName in campDict.keys():
            if campDict[campName][5] != 0:
                append_this = campDict[campName]
                append_this.insert(0, campName)
                final_list.append(append_this)
        print(final_list)

        return final_list

    # -------------------------------------------------------------------------------------------------

    def readItemAvailability(self, district, item, itm_type):
        """ find if an item is available in any camp [in a given district] """

        # get a list of all databases (camps, other default db)
        print("in readItemAvail()")
        db_list = self.listAllDatabases()

        # os.system("cls")
        # print relevant header
        if itm_type == "medical":
            header = "(campName, district, city_or_village, item_name, item_type, description, age_groups, qty)\n"
        else:
            header = "(campName, district, city_or_village, item_name, item_type, description, qty)\n"
        print(header)

        availCampList = list()
        data = list()
        for campName in db_list:
            if campName[0:4] == 'camp':  # if it is a camp only then proceed
                cur, conn = self.connect(str(campName))
                # initial check to ensure camp is from same district and same year
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
                    print(query)

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
                            data.append(row)
                            # print the updated row
                            print(row)
                        print()
        return data

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
    def requestSupplyFromMain(self, campName, data: tuple):
        """ send supply request to govt(sysAdmin) team """

        campId = campName[4:]
        # get item details
        itmName = data[0].lower()

        itmType = data[1].lower()

        itmDescription = data[2]
        qty = data[3]

        # demand table
        tableName = "demand" + CampAdmin.thisYear
        # query to insert the demanded item in demand table
        query = "insert into " + tableName + " values('" + campId + "', '" + \
                itmName + "', '" + itmType + "', '" + itmDescription + "', " + qty + ");"
        # connect to all camp database (common/general database)
        cur, conn = self.connect("all_camp_details")
        cur.execute(query)  # make the demand (insert the demand in table)

        rowcount = cur.rowcount
        cur.close()
        conn.close()
        if rowcount == 1:
            print("Request Successfully submitted.")
            return "Request Successfully submitted."
        else:
            print("There was an ERROR in submission of report !!")
            print("Try again...")
            return "There was an ERROR in submission of report !!"
        print()

    # -------------------------------------------------------------------------------------------------

    def updateSupplyData(self, campName: str, data: tuple):
        """ add/update the supply records in camp """
        cur, conn = self.connect(campName)

        # first get basic things
        itemName = data[0].lower()
        category = data[1].lower()
        quantity = data[5]

        # select appropriate table
        tableName = category + "_supply_table" + CampAdmin.thisYear
        query = "select item_name from " + tableName + ";"
        cur.execute(query)

        # get list of all items already present
        allItems = cur.fetchall()
        listOfItems = list()
        for itm in allItems:
            listOfItems.append(itm[0])
        print(listOfItems)

        # if the item is already present, then update it's quantity
        if itemName in listOfItems:
            # create and execute the query
            query = "update " + tableName + " set qty = " + quantity + " where item_name = '" + itemName + "';"
            cur.execute(query)
            print()

            rowcount = cur.rowcount
            cur.close()
            conn.close()

            if rowcount == 1:
                print("Successfully updated record")
                return "Successfully updated record"
            else:
                print("There was an ERROR in updating the record !! Try again.")
                return "There was an ERROR in updating the record !!\nTry again."
        else:
            # if data item is not present already, then create a new entry for it
            ageGroups = data[2].lower()
            itemDescription = data[4].lower()
            itemType = data[3].lower()

            # query created according to category
            if category == "medical":
                query = "insert into " + tableName + " values('" + itemName + "', '" + \
                        itemType + "', '" + itemDescription + "', '" + ageGroups + "', " + quantity + ");"
            else:
                query = "insert into " + tableName + " values('" + itemName + "', '" + \
                        itemType + "', '" + itemDescription + "', " + quantity + ");"
            # connect to camp database & execute query

            print(query)
            cur, conn = self.connect(campName)
            cur.execute(query)
            print()

            rowcount = cur.rowcount
            cur.close()
            conn.close()

            if rowcount == 1:
                print("Successfully added record")
                return "Successfully added record"
            else:
                print("There was an ERROR in adding the record !! Try again.")
                return "There was an ERROR in adding the record !! \nTry again."

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
