from Database import Database
from datetime import datetime


def cleanFirst(dbase) -> None:
    cur, conn = dbase.connect()
    cur.execute("DROP database camp27b4677;")
    cur.execute("Drop database all_camp_details;")
    print("Cleaned !")

def createTestDatabases(dbase) -> str:
    log = open("logfile.log", "a")
    cur, conn = dbase.connect()
    base_db = "CREATE DATABASE all_camp_details;"
    cur.execute(base_db)
    log.write("[+] all_camp_details\n")

    test_db1 = "CREATE DATABASE camp27b4677;"
    cur.execute(test_db1)
    log.write("[+] camp27b4677\n")

    cur.close()
    conn.close()
    log.close()
    return "skeleton created"


def populateTestDatabases(dbase) -> str:
    log = open("logfile.log", "a")
    base_db = "all_camp_details"
    cur, conn = dbase.connect(base_db)

    # thisYear = str(datetime.now().year)
    thisYear = "2021"

    # populate base database with tables
    log.write("\n\n=> all_camp_details: \n")
    campDetailsTableName = "campdet" + thisYear
    createCampDetailsTable = "create table " + campDetailsTableName + "( \
            camp_id varchar(20) primary key, \
            camp_name varchar(20) not null, \
            state varchar(20) not null, \
            district varchar(20) not null, \
            city_or_village varchar(20) not null, \
            coordinates varchar(50) not null, \
            camp_admin varchar(20) not null, \
            camp_admin_aadhar varchar(12) unique not null, \
            email varchar(25) not null, \
            mobile varchar(10) not null, \
            total_camp_capacity int not null, \
            capacity_full char(1) not null  \
            );"
    cur.execute(createCampDetailsTable)
    log.write("[+] campdet2021\n")

    supportMembersTableName = "support_members" + thisYear
    createSupportMembersTable = "create table " + supportMembersTableName + "( \
                    camp_id varchar(20) not null, \
                    Support_member varchar(20) not null, \
                    member_aadhar varchar(12) unique not null, \
                    email varchar(25) not null, \
                    mobile varchar(10) not null, \
                    foreign key (camp_id) references campdet2021(camp_id) \
                    );"
    cur.execute(createSupportMembersTable)
    log.write("[+] support_members2021\n")

    feebackTableName = "feedback" + thisYear
    createFeedbackTable = "create table " + feebackTableName + "( \
                    camp_id varchar(20) primary key references campdet2021(camp_id), \
                    feedback text not null \
                    );"
    cur.execute(createFeedbackTable)
    log.write("[+] feedback2021\n")

    demandTableName = "demand" + thisYear
    createDemandTable = "create table " + demandTableName + "( \
                camp_id varchar(20) not null references campdet2021(camp_id),\
                item_name varchar(40) not null,\
                item_type varchar(10) not null,\
                item_description varchar(100),\
                qty integer not null\
                );"
    cur.execute(createDemandTable)
    log.write("[+] demand2021\n")

    cur.close()
    conn.close()

    # connect to test camp 1
    log.write("\n=>camp27b4677: \n\n")
    cur, conn = dbase.connect("camp27b4677")

    mainTableName = "main_table" + thisYear
    createMainTable = "create table " + mainTableName + "(\
                family_id varchar(20) not null,\
                member_no int not null,\
                name varchar(40) not null,\
                age int not null,\
                gender char(1) not null,\
                relation varchar(10) not null,\
                vill_or_city varchar(50) not null,\
                loc_in_vill_or_city varchar(70) not null,\
                inCamp char(1) not null,\
                joinedOn date,\
                leftOn date,\
                injury char(1) not null,\
                primary key (family_id, member_no)\
                );"
    cur.execute(createMainTable)
    log.write("[+] main_table2021\n")

    injuryTableName = "injury_table" + thisYear
    createInjuryTable = "create table " + injuryTableName + "(\
                    family_id varchar(20) not null,\
                    member_no int not null,\
                    injury_description varchar(200) not null,\
                    injury_level char(1) not null,\
                    recovery_initiated char(1) not null,\
                    recovery_percent int not null,\
                    foreign key(family_id, member_no) references main_table2021\
                    );"
    cur.execute(createInjuryTable)
    log.write("[+] injury_table2021\n")

    regularSupplyTableName = "regular_supply_table" + thisYear
    createRegularSupplyTable = "create table " + regularSupplyTableName + "(\
                    item_name varchar(50) not null primary key,\
                    item_type varchar(20) not null,\
                    description varchar(100) not null,\
                    qty int not null\
                    );"
    cur.execute(createRegularSupplyTable)
    log.write("[+] regular_supply_table2021\n")

    medicalSupplyTable = "medical_supply_table" + thisYear
    createMedicalSupplyTable = "create table " + medicalSupplyTable + "(\
                        item_name varchar(50) not null primary key,\
                        item_type varchar(20) not null,\
                        description varchar(100) not null,\
                        age_groups varchar(10) not null,\
                        qty int not null\
                        );"
    cur.execute(createMedicalSupplyTable)
    log.write("[+] medical_supply_table2021\n")

    myCampInfoTable = "my_camp_info"
    createMyCampInfoTable = "create table " + myCampInfoTable + "(\
                    camp_id varchar(20) not null,\
                    camp_name varchar(20) not null,\
                    state varchar(20) not null,\
                    district varchar(20) not null,\
                    city_or_village varchar(20) not null,\
                    coordinates varchar(50) not null,\
                    camp_admin varchar(20) not null,\
                    camp_admin_aadhar varchar(12) unique not null,\
                    email varchar(25) not null,\
                    mobile varchar(10) not null,\
                    total_camp_capacity int not null,\
                    capacity_full char(1) not null,\
                    month varchar(2) not null,\
                    year varchar(4) not null,\
                    primary key(month,year)\
                    );"
    cur.execute(createMyCampInfoTable)
    log.write("[+] my_camp_info\n")

    todayAllView = "create view today_all as " + \
                   "select family_id, member_no, name, age, gender, relation," + \
                   " vill_or_city, loc_in_vill_or_city, incamp " + \
                   "from main_table2021 where joinedon = current_date;"
    cur.execute(todayAllView)
    log.write("[+] today_all\n")
    cur.close()
    conn.close()
    log.close()
    return "populated structures successfully"


def populateTestTables(dbase) -> str:
    log = open("logfile.log", "a")
    log.write("\nInserting values in [all_camp_details]: \n\n")
    base_db = "all_camp_details"
    cur, conn = dbase.connect(base_db)

    # inserting in base_db
    inCampDetails = "insert into campdet2021 values" + \
                    "('27b4677','camp27b4677','Assam','Lakhimpur','Narayanpur'," + \
                    "'26.950841, 93.859420','Narayan','123456789876','example@main.com'," + \
                    "'1234567890', 400,'N');"
    cur.execute(inCampDetails)
    log.write("into=> campdet2021\n")

    inSupportMembers = "insert into support_members2021 values(" + \
                       "'27b4677', 'Lokesh','243567898567','email@mail.com','1234567890');"
    cur.execute(inSupportMembers)
    log.write("into=> support_members2021\n")
    inSupportMembers = "insert into support_members2021 values(" + \
                       "'27b4677', 'Pratap','243567432267','email@mail.com','1234567890');"
    cur.execute(inSupportMembers)
    log.write("into=> support_members2021\n")

    inFeedback = "insert into feedback2021 values('27b4677','This is a feedback.');"
    cur.execute(inFeedback)
    log.write("into=> feedback2021\n")

    inDemand = "insert into demand2021 values('27b4677', 'pcm 500 mg'," + \
               " 'medical', 'relieve from fever, headache',500);"
    cur.execute(inDemand)
    log.write("into=> demand2021\n")

    cur.close()
    conn.close()

    # inserting in test 1
    log.write("\nInserting values in [camp27b4677]: \n\n")
    cur, conn = dbase.connect("camp27b4677")

    inMainTable = "insert into main_table2021 values(" + \
                  "'FLY1001', 1, 'DemoName', 35, 'M','self','Narayanpur'," + \
                  "'near Hariram', 'Y', '2021-10-21', null, 'Y');"
    cur.execute(inMainTable)
    log.write("into=> main_table2021\n")
    inMainTable = "insert into main_table2021 values(" + \
                  "'FLY1001', 2, 'Person2', 40, 'M','brother','Narayanpur'," + \
                  "'near Hariram', 'N', '2021-10-21', null, 'Y');"
    cur.execute(inMainTable)
    log.write("into=> main_table2021\n")
    inMainTable = "insert into main_table2021 values(" + \
                  "'FLY1002', 1, 'xgcds', 48, 'M','self','Narayanpur','near Hariram'," + \
                  " 'Y', '2021-10-22', null, 'Y');"
    cur.execute(inMainTable)
    log.write("into=> main_table2021\n")

    inInjuryTable = "insert into injury_table2021 values(" + \
                    "'FLY1001', 1, 'xyz bone fracture', 'L', 'Y', 10);"
    cur.execute(inInjuryTable)
    log.write("into=> injury_table2021\n")
    inInjuryTable = "insert into injury_table2021 values(" + \
                    "'FLY1002', 1, 'xyz bone fracture', 'L', 'Y', 54);"
    cur.execute(inInjuryTable)
    log.write("into=> injury_table2021\n")

    inMedicalSupply = "insert into medical_supply_table2021 values(" + \
                      "'PCM 500mg','tab','used to relieve headache, fever, and pain in body'," + \
                      "'all',800);"
    cur.execute(inMedicalSupply)
    log.write("into=> medical_supply_table2021\n")

    inMyCamp = "insert into my_camp_info values(" + \
               "'27b4677','camp27b4677','Assam','Lakhimpur','Narayanpur','26.950841, 93.859420','Narayan'" + \
               ",'123456789876','example@main.com','1234567890', 400,'N','10','2021');"
    cur.execute(inMyCamp)
    log.write("into=> my_camp_details")

    cur.close()
    conn.close()
    log.close()
    return "tables populated successfully"


def main():
    # try except finally
    dbase = Database()
    try:
        cur, conn = dbase.connect()
        print("Connection Successful !")

        cur.execute("select version()")
        version = cur.fetchone()[0]
        print(version)

        cur.close()
        conn.close()
    except:
        print("Error, can't connect with Postgre SQL. Ensure it is correctly installed!!!")
        exit()

    print("\nThis will erase any pre-existing database in [all_camp_details, camp27b4677]")
    clean = input("Are you sure you want to proceed(y/n)? ").lower()
    if clean == 'y':
        cleanFirst(dbase)

        file = open("logfile.log", "w")
        file.close()
        response = createTestDatabases(dbase)
        print(response)

        response = populateTestDatabases(dbase)
        print(response)

        response = populateTestTables(dbase)
        print(response)

        print("\ncheck the logfile.log for more details")
    else:
        print("Operation aborted!!")

if __name__ == "__main__":
    main()
