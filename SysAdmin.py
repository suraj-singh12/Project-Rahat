from Database import Database
import datetime


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

    def __setCampDetails(self, campName):
        """ sets the camp details in all_camp_details database """
        print("Enter the below information correctly: ")
        campId = campName[4:]
        # campName we already have

        print("=> Enter Location Details: ")
        state = input("State: ")
        # check method will be installed later
        district = input("District: ")
        cityOrVillage = input("city/village name: ")
        coord = input("Coordinates: ")
        while len(coord) > 50:
            print("Error, Coordinates length exceeds max length! Try again")
            coord = input("Coordinates: ")

        print("=> Enter Camp Admin Details: ")
        campAdminName = input("Name: ")
        campAdminAadhar = input("Aadhar: ")
        while len(campAdminAadhar) != 12:
            print("Error, invalid Aadhar number. Try again")
            campAdminAadhar = input("Aadhar: ")

        email = input("Email: ")
        phone = input("Phone Number: ")
        while len(phone) != 10:
            print("Error, invalid phone number. Enter 10 digit valid phone number")
            phone = input("Phone Number: ")

        print("=> Camp Related")
        totalCampCapacity = input("Total capacity of camp (in numbers): ")
        capacityFull = 'N'

        cur, conn = self.connect("all_camp_details")
        # insert in main table (campdetYEAR)
        tableName = "campdet" + SysAdmin.thisYear

        query_data = "'" + campId + "', '" + campName + "', '" + state + "', '" + district + "', '" + \
                     cityOrVillage + "', '" + coord + "', '" + campAdminName + "', '" + \
                     campAdminAadhar + "', '" + email + "', '" + phone + "', " + totalCampCapacity + \
                     ", '" + capacityFull + "'"

        query = "INSERT INTO " + tableName + " values (" + query_data + ");"
        cur.execute(query)

        # get support member details here 
        print("Enter the support member details: ")
        while True:
            memberName = input("Enter member name: ")
            memberAadhar = input("Enter member Aadhar Number: ")
            while (memberAadhar.isdigit() is False) or (len(memberAadhar) != 12):
                print("Error, invalid Aadhar number. Enter a 12 digit aadhar.")
                memberAadhar = input("Enter member Aadhar Number: ")
            memberEmail = input("Enter member Email: ")
            memberMobile = input("Enter member Mobile Number: ")
            while (memberAadhar.isdigit() is False) or (len(memberMobile) != 10):
                print("Error, invalid mobile number. Enter a 10 digit number.")
                memberMobile = input("Enter member Mobile Number: ")

            supportTableName = "support_members" + SysAdmin.thisYear
            insertInSupportTable = "insert into " + supportTableName + " values('" + \
                                   campId + "', '" + memberName + "', '" + memberAadhar + \
                                   "', '" + memberEmail + "', '" + memberMobile + "');"
            cur.execute(insertInSupportTable)

            choice = input("More members?(y/n) ").lower()
            if choice != 'y':
                break

        print("Total rows affected = {}".format(cur.rowcount))
        cur.close()
        conn.close()
        return query_data

    # -----------------------------------------------------------------------------------------------------------------------------

    def __removeCampDetails(self, campName):
        cur, conn = self.connect("all_camp_details")
        # remove details from support table
        supportTableName = "support_members" + SysAdmin.thisYear
        removeFromSupport = "Delete from " + supportTableName + " where campid = '" + campName[4:] + "';"
        cur.execute(removeFromSupport)

        # remove details from main table
        tableName = "campdet" + SysAdmin.thisYear
        removeFromCampdet = "Delete from " + tableName + " where campId = '" + campName[4:] + "';"
        cur.execute(removeFromCampdet)

        print("Total rows affected = {}".format(cur.rowcount))
        cur.close()
        conn.close()

    # -----------------------------------------------------------------------------------------------------------------------------

    def registerCamp(self):
        """ in technical terms: Creates a new database for a new camp,
        fills it will all the required tables, sets this camp details in all_camp_details """

        inp = input("Enter camp ID: ").lower()
        campName = "camp" + inp

        if not self.isPresentCamp(campName):
            query_data = self.__setCampDetails(campName)

            # connect to default database
            cur, conn = self.connect()

            # create database campName
            createDatabase = "CREATE DATABASE " + campName + ";"
            cur.execute(createDatabase)
            cur.close()
            conn.close()

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
            createMyCampInfoTable = "create table " + myCampInfoTableName + """(
                                        campID varchar(20) not null,
                                        campName varchar(20) not null,
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
            # fill my camp info using query_data variable

            TodayAll = "today_all"  # a view on main_tableYEAR
            createViewTodayAll = "create view " + TodayAll + " as " + \
                                 "select family_id, member_no, name, age, gender, " \
                                 "relation, vill_or_city, loc_in_vill_or_city, incamp " \
                                 "from " + mainTableName + ", current_date where joinedon = current_date;"
            cur.execute(createViewTodayAll)

            print("Camp " + campName + " successfully registered.")
            cur.close()
            conn.close()
        else:
            print("Camp " + campName + " already exists!!")

    # -----------------------------------------------------------------------------------------------------------------------------
    def deRegister(self):
        """ in technical terms: drop a database"""

        inp = input("Enter camp ID: ").lower()
        campName = "camp" + inp

        if self.isPresentCamp(campName):
            # https://stackoverflow.com/questions/13719674/change-database-postgresql-in-python-using-psycopg2-dynamically

            # connect to required camp database
            cur, conn = self.connect(campName)
            # find all existing relations/tables in database
            cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")

            if cur.rowcount == 0:
                print("No relation found in " + campName)
            else:
                print("\nAll these relations exist in " + campName + " :")
                for table in cur.fetchall():
                    print(table[2], end=' ')

            print("\n\n[Note: This action is irreversible and you will lose all the data of this camp]")
            consent = input("\nAre you sure you want to de-register this camp?(y/n): ")

            if consent.lower() == 'y':
                # close connection with current database
                cur.close()
                conn.close()
                # connect to default database
                cur, conn = self.connect()
                # drop the desired database
                cur.execute("DROP DATABASE " + campName + ";")

                # also remove it's information from all_camps_details
                self.__removeCampDetails(campName)
                print("Successfully de-registered " + campName)
            else:
                print("Operation Aborted!")
                # close connection with whatever database is connected
            cur.close()
            conn.close()
        else:
            print("Error! There is no camp as " + campName)

    # -----------------------------------------------------------------------------------------------------------------------------
    def readCamp(self):
        """ Read data of any camp by campID """

        inp = input("Enter the camp ID: ")
        campName = "camp" + inp
        # campName = inp        # uncomment this to access testingBase database and comment out above line

        if self.isPresentCamp(campName):
            # connect to required camp database
            cur, conn = self.connect(campName)
            # find all existing relations/tables in database
            cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")

            if cur.rowcount == 0:
                print("NO relation found in " + campName)
            else:
                print("\nRelations of " + campName + " :")
                print("==> ", end='')

                all_relations = list()
                # print all the relations in current database
                for table in cur.fetchall():
                    # print(table)
                    print(table[2], end=', ')  # prints the table name only
                    all_relations.append(table[2])
                print()

                relation = input("Enter the relation name you want to access: ")

                # if the relation is present then print its data, else say not found
                if relation in all_relations:
                    print("Data of " + relation + ": ")
                    cur.execute("select * from " + relation + ";")
                    for row in cur.fetchall():
                        print(row)
                else:
                    print("Error, " + relation + " not found! Please select an existing relation")

            cur.close()
            conn.close()
        else:
            print("Error! " + campName + " is not a registered camp")

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
            header = ["campId", "campName", "state", "district", "city_or_village", "coordinates", "Admin",
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
                header = ["campId", "campName", "state", "district", "city_or_village", "coordinates", "Admin",
                          "Admin_Aadhar", "email", "phone", "Total Capacity", "Capacity Full?"]
                for item in header:
                    print(item, end='\t')
                print()

                idd = myCamp[4:]
                # find details of current camp
                cur.execute("select * from " + tableName + " where campId = '" + idd + "' ;")
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

                cur.execute("select * from support_members" + SysAdmin.thisYear + " where campId = '" + idd + "';")
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
