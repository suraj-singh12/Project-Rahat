import GetMemberDetails_UI
from Database import Database
import datetime
import GetCampDetails_UI
from PyQt5 import QtWidgets
import SelectTableToRead_UI
import MainTable2021_UI
import InjuryTable2021_UI
import RegularSupplyTable_UI
import MedicalSupplyTable_UI
import TodayAll_UI
import MyCampInfo_UI
import AllCampDetails_UI


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


class InjuryTable(QtWidgets.QMainWindow, InjuryTable2021_UI.Ui_MainWindow):
    def __init__(self):
        super(InjuryTable, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class RegularSupply(QtWidgets.QMainWindow, RegularSupplyTable_UI.Ui_MainWindow):
    def __init__(self):
        super(RegularSupply, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class MedicalSupply(QtWidgets.QMainWindow, MedicalSupplyTable_UI.Ui_MainWindow):
    def __init__(self):
        super(MedicalSupply, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class TodayAll(QtWidgets.QMainWindow, TodayAll_UI.Ui_MainWindow):
    def __init__(self):
        super(TodayAll, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class MyCamp(QtWidgets.QMainWindow, MyCampInfo_UI.Ui_MainWindow):
    def __init__(self):
        super(MyCamp, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class AllCampDet(QtWidgets.QMainWindow, AllCampDetails_UI.Ui_MainWindow):
    def __init__(self):
        super(AllCampDet, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton.clicked.connect(self.ok_clicked)

    def ok_clicked(self):
        # close the window
        self.close()


class GetDetails(QtWidgets.QWidget, GetCampDetails_UI.Ui_Dialog):
    def __init__(self):
        super(GetDetails, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton_2.setAutoDefault(True)


class GetMemDetails(QtWidgets.QWidget, GetMemberDetails_UI.Ui_Dialog):
    def __init__(self):
        super(GetMemDetails, self).__init__()
        self.setupUi(self)
        self.pushButton.setAutoDefault(True)
        self.pushButton_2.setAutoDefault(True)


class SysAdmin(Database):
    """ -------- System Admin portal functions -------- """

    usrType = "sys_admin"
    identity = "sysadmin"
    thisYear = str(datetime.datetime.now().year)

    # -----------------------------------------------------------------------------------------------------------------------------
    def __init__(self, pswd):
        if not self.validate(SysAdmin.usrType, SysAdmin.identity, pswd):
            print("Authentication Failed !")
            exit(-1)

    # -----------------------------------------------------------------------------------------------------------------------------

    def __setCampDetails(self, campName, camp_data, member_data):
        """ sets the camp details in all_camp_details database """
        print("Enter the below information correctly: ")
        campId = campName[4:]

        state = camp_data[0]
        district = camp_data[1]
        cityOrVillage = camp_data[2]
        coord = camp_data[3]

        campAdminName = camp_data[4]
        campAdminAadhar = camp_data[5]
        email = camp_data[6]
        phone = camp_data[7]
        totalCampCapacity = camp_data[9]
        capacityFull = 'N'

        print(camp_data)

        cur, conn = self.connect("all_camp_details")
        # insert in main table (campdetYEAR)
        tableName = "campdet" + SysAdmin.thisYear

        query_data = "'" + campId + "', '" + campName + "', '" + state + "', '" + district + "', '" + \
                     cityOrVillage + "', '" + coord + "', '" + campAdminName + "', '" + \
                     campAdminAadhar + "', '" + email + "', '" + phone + "', " + totalCampCapacity + \
                     ", '" + capacityFull + "'"
        print(query_data)

        query = "INSERT INTO " + tableName + " values (" + query_data + ");"
        cur.execute(query)

        print("Query done")

        # get support member details here
        i = 0
        while i < len(member_data):
            memberName = member_data[i][0]
            memberAadhar = member_data[i][1]
            memberEmail = member_data[i][2]
            memberMobile = member_data[i][3]
            i += 1

            supportTableName = "support_members" + SysAdmin.thisYear
            insertInSupportTable = "insert into " + supportTableName + " values('" + \
                                   campId + "', '" + memberName + "', '" + memberAadhar + \
                                   "', '" + memberEmail + "', '" + memberMobile + "');"
            print(insertInSupportTable)
            cur.execute(insertInSupportTable)

        print("Total rows affected = {}".format(cur.rowcount))
        cur.close()
        conn.close()
        return query_data

    # -----------------------------------------------------------------------------------------------------------------------------

    def __removeCampDetails(self, campName):
        cur, conn = self.connect("all_camp_details")
        # remove details from support table
        supportTableName = "support_members" + SysAdmin.thisYear
        removeFromSupport = "Delete from " + supportTableName + " where camp_id = '" + campName[4:] + "';"
        cur.execute(removeFromSupport)

        # remove details from main table
        tableName = "campdet" + SysAdmin.thisYear
        removeFromCampdet = "Delete from " + tableName + " where camp_id = '" + campName[4:] + "';"
        cur.execute(removeFromCampdet)

        print("Total rows affected = {}".format(cur.rowcount))
        cur.close()
        conn.close()

    # -----------------------------------------------------------------------------------------------------------------------------

    def registerCamp(self, campName, camp_data, member_data):
        """ in technical terms: Creates a new database for a new camp,
        fills it will all the required tables, sets this camp details in all_camp_details """

        if not self.isPresentCamp(campName):
            query_data = self.__setCampDetails(campName, camp_data, member_data)
            print(query_data)

            # connect to default database
            cur, conn = self.connect()

            # create database campName
            createDatabase = "CREATE DATABASE " + campName + ";"
            cur.execute(createDatabase)
            cur.close()
            conn.close()
            print("Database " + campName + "created successfully")

            # connect with new database (camp)
            cur, conn = self.connect(campName)

            # fill the camp with required tables
            mainTableName = "main_table" + SysAdmin.thisYear
            createMainTable = "create table " + mainTableName + """(
                                family_id varchar(20) not null, 
                                member_no int not null,
                                name varchar(40) not null,
                                age int not null,
                                gender char(1) not null,
                                relation varchar(10) not null,
                                vill_or_city varchar(50) not null,
                                loc_in_vill_or_city varchar(70) not null,
                                inCamp char(1) not null,
                                joinedOn date,
                                leftOn date,
                                injury char(1) not null,
                                primary key (family_id, member_no)
                                );"""
            cur.execute(createMainTable)

            injuryTableName = "injury_table" + SysAdmin.thisYear
            createInjuryTable = "create table " + injuryTableName + """(
                                family_id varchar(20) not null,
                                member_no int not null,
                                injury_description varchar(200) not null,
                                injury_level char(1) not null,
                                recovery_initiated char(1) not null,
                                recovery_percent int not null,
                                foreign key(family_id, member_no) references main_table2021
                                );"""
            cur.execute(createInjuryTable)

            regularSupplyTableName = "regular_supply_table" + SysAdmin.thisYear
            createRegularSupplyTable = "create table " + regularSupplyTableName + """(
                                        item_name varchar(50) not null primary key,
                                        item_type varchar(20) not null,
                                        description varchar(100) not null,
                                        qty int not null
                                        );"""
            cur.execute(createRegularSupplyTable)

            medicalSupplyTableName = "medical_supply_table" + SysAdmin.thisYear
            createMedicalSupplyTable = "create table " + medicalSupplyTableName + """(
                                        item_name varchar(50) not null primary key,
                                        item_type varchar(20) not null,
                                        description varchar(100) not null,
                                        age_groups varchar(10) not null,
                                        qty int not null
                                        );"""
            cur.execute(createMedicalSupplyTable)

            myCampInfoTableName = "my_camp_info"
            print(myCampInfoTableName)
            createMyCampInfoTable = "create table " + myCampInfoTableName + """(
                                        camp_id varchar(20) not null,
                                        camp_name varchar(20) not null,
                                        state varchar(20) not null,
                                        district varchar(20) not null,
                                        city_or_village varchar(20) not null,
                                        coordinates varchar(50) not null,
                                        camp_admin varchar(20) not null,
                                        camp_admin_aadhar varchar(12) unique not null,
                                        email varchar(25) not null,
                                        mobile varchar(10) not null,
                                        total_camp_capacity int not null,
                                        capacity_full char(1) not null,
                                        month varchar(2) not null,
                                        year varchar(4) not null,
                                        primary key(month,year)
                                        );"""
            cur.execute(createMyCampInfoTable)
            month = str(datetime.datetime.now())[5:7]
            query_data = query_data + ",'" + month + "','" + SysAdmin.thisYear + "'"
            insertInMyCampInfoTable = "INSERT INTO " + myCampInfoTableName + " values (" + query_data + ");"
            cur.execute(insertInMyCampInfoTable)

            TodayAll = "today_all"  # a view on main_tableYEAR
            createViewTodayAll = "create view " + TodayAll + " as " + \
                                 "select family_id, member_no, name, age, gender, " \
                                 "relation, vill_or_city, loc_in_vill_or_city, incamp " \
                                 "from " + mainTableName + ", current_date where joinedon = current_date;"
            cur.execute(createViewTodayAll)

            print("Camp " + campName + " successfully registered.")
            cur.close()
            conn.close()
            return 0
        else:
            print("Camp " + campName + " already exists!!")
            return 1

    # -----------------------------------------------------------------------------------------------------------------------------
    def deRegister_step1(self, campName):
        """ in technical terms: drop a database"""
        print("in")
        if self.isPresentCamp(campName):
            # connect to required camp database
            cur, conn = self.connect(campName)
            # find all existing relations/tables in database
            cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")

            print("before rowcount")
            if cur.rowcount == 0:
                print("No relation found in " + campName)
                cur.close()
                conn.close()
                message = "No relation found in " + campName
                message += '\n' + "Are You sure you want to de-register this camp?\n"
                return message

            print("\nAll these relations exist in " + campName + " :")
            all_relations = ''
            for table in cur.fetchall():
                print(table[2], end=' ')
                all_relations += str(table[2]) + '\n'
            cur.close()
            conn.close()
            message = "All these relations exist in " + campName + '\n' + all_relations
            message += '\n' + "Are You sure you want to de-register this camp?\n"
            return message
        else:
            return -1

    def deRegister_step2(self, campName):
            print("\n\n[Note: This action is irreversible and you will lose all the data of this camp]")
            try:
                cur, conn = self.connect()
                # drop the desired database
                cur.execute("DROP DATABASE " + campName + ";")
                print("database removed (but not info)")

                # also remove it's information from all_camps_details
                self.__removeCampDetails(campName)
                print("Successfully de-registered " + campName)
                cur.close()
                conn.close()
                return 0
            except:
                print("Error, could not de-register " + campName)
                return 1

    # -----------------------------------------------------------------------------------------------------------------------------
    def readCamp(self, campName):
        """ Read data of any camp by campID """

        if self.isPresentCamp(campName):
            # connect to required camp database
            cur, conn = self.connect(campName)
            # find all existing relations/tables in database
            cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")

            if cur.rowcount == 0:
                print("NO relation found in " + campName)
                cur.close()
                conn.close()
                message = "No relation found in " + campName
                t = list()
                t.append(message)
                t.append('')
                return tuple(t)      # show on grey label

            print("\nRelations of " + campName + " :")
            print("==> ", end='')

            all_relations = ''
            all_relations_list = []
            # print all the relations in current database
            for table in cur.fetchall():
                # print(table)
                print(table[2], end=', ')  # prints the table name only
                all_relations += table[2] + '\n'
                all_relations_list.append(table[2])
            print()
            cur.close()
            conn.close()
            message = "All these relations exist in " + campName + '\n\n' + all_relations
            t = list()
            t.append(message)
            t.append(all_relations_list)
            # print(t)
            return tuple(t)
        else:
            t = list()
            t.append('-1')
            return tuple(t)

    # -----------------------------------------------------------------------------------------------------------------------------

    def listAllRegCampsInfo(self):
        """ Lists out the information of all registered camps by specific year """

        cur, conn = self.connect("all_camp_details")

        year = input("Enter the year of which camps you want to access (yyyy): ")
        while (len(year) != 4) or (year.isnumeric() is False) or (year[0:3] != "202"):
            print("Try again.. It is not a valid year.")
            year = input("Enter the year of which camps you want to access (yyyy):")
        tableName = "campdet" + year

        print()
        # selection menu
        print("1. Print campNames only")
        print("2. Print details of all camps")
        print("3. Print full details of a specific camp")
        choice = int(input("Enter your choice: "))
        print()

        if choice == 1:
            print("All camps registered in 2021 are: ")
            cur.execute("select * from " + tableName + ";")

            # printing camp names
            for item in cur.fetchall():
                print(item[1], end='\t')
            print()

        elif choice == 2:
            print("Details of all camps registered in year 2021: ")
            header = ["camp_id", "camp_id", "state", "district", "city_or_village", "coordinates", "Admin",
                      "Admin_Aadhar", "email", "phone", "Total Capacity", "Capacity Full?"]
            for item in header:
                print(item, end='\t')
            print()

            cur.execute("select * from " + tableName + ";")
            # printing details of all camps of entered year
            for row in cur.fetchall():
                for item in row:
                    print(item, end='\t')
                print()

        elif choice == 3:
            print("All camps registered in year " + SysAdmin.thisYear + " are: ")
            cur.execute("select * from " + tableName + ";")
            camps = []
            for item in cur.fetchall():
                camps.append(item[1])
                print(item[1], end=', ')
            print()

            myCamp = input("Enter the camp Name: ")
            if myCamp not in camps:
                print("Error, no such camp exists !")
                return
            else:
                """ print the details of the camp with details of support members too """

                print()
                header = ["camp_id", "camp_id", "state", "district", "city_or_village", "coordinates", "Admin",
                          "Admin_Aadhar", "email", "phone", "Total Capacity", "Capacity Full?"]
                for item in header:
                    print(item, end='\t')
                print()

                idd = myCamp[4:]
                # find details of current camp
                cur.execute("select * from " + tableName + " where camp_id = '" + idd + "' ;")
                # print details of this camp
                for row in cur.fetchall():
                    for item in row:
                        print(item, end='\t')
                    print()

                print()

                # print details of support members
                header = ["Member Name", "Member Aadhar", "email", "phone"]
                for item in header:
                    print(item, end="\t")
                print()

                cur.execute("select * from support_members" + SysAdmin.thisYear + " where camp_id = '" + idd + "';")
                for row in cur.fetchall():
                    for item in row[1:]:
                        print(item, end='\t')
                    print()
                print()
        else:
            print("Invalid Choice !")

        cur.close()
        conn.close()
# -----------------------------------------------------------------------------------------------------------------------------
