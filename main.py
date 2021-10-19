# RAHAT v1.0

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# important to import and enable isolation_level_autocommot otherwise database creation fails

# usrname = "postgres"
# psswd = "toor"

# conn = psycopg2.connect(
#     host="localhost",
#     database="testingbase",
#     user=usrname,
#     password=psswd)

from config import config

def connect(database=''):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print('\nConnecting to the PostgreSQL database...')   #-----------
        if database != '':      # if a database is specified during connection, then connect to that otherwise default
            params['database'] = database
        
        conn = psycopg2.connect(**params)

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # enabled isolation_level_autocommit ; now databases can be created without issue

        # print("Connected successfully.\n")    #-----------
        # create a cursor
        cur = conn.cursor()
        
	    # execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version();')

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
        
        # printing tables of 'testingbase' database
        # print('\ntestingbase tables :')
        # cur.execute("""SELECT * FROM information_schema.tables WHERE table_schema = 'public'""")
        # for table in cur.fetchall():
        #     print(table[2])
        # print()

        # print the contents of students
        # cur.execute('select * from students')
        # for tupl in cur.fetchall():
        #     print(tupl)
       
	    # close the communication with the PostgreSQL
        # cur.close()
        return cur,conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')


''' -------- System Admin portal functions -------- '''

def registerCamp():
    """ in technical terms: Creates a new database for a new camp """
    inp = input("Enter camp ID: ").lower()
    campName = "camp" + inp
    
    # connect to database
    cur,conn = connect()
    # list all databases
    cur.execute("SELECT datname FROM pg_database;")
    db_list = list()
    for db in cur.fetchall():
        db_list.append(db[0])
    
    # search in them if campName database exists or not, if not, then create
    if campName not in db_list:
        createDatabase = "CREATE DATABASE " + campName + ";"
        cur.execute(createDatabase)
        print("Camp " + campName + " successfully registered.")
    else:
        print("Camp " + campName + " already exists!!")
    
    # dispose the cursor
    cur.close()
    # close the connection
    conn.close()


def deRegister():
    """ in technical terms: drop a database"""
    inp = input("Enter camp ID: ").lower()
    campName = "camp" + inp
    
    # connect to default database
    cur,conn = connect()
    # list all databases
    cur.execute("SELECT datname FROM pg_database;")
    db_list = list()
    for db in cur.fetchall():
        db_list.append(db[0])
    
    if campName in db_list:
        # https://stackoverflow.com/questions/13719674/change-database-postgresql-in-python-using-psycopg2-dynamically
        cur.close()
        conn.close()

        # connect to required camp database
        cur,conn = connect(campName)
        # find all existing relations/tables in database
        cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
        
        
        if cur.rowcount == 0:
            print("No relation found in " + campName)
        else:
            print("All these relations exist in " + campName + " :")
            for table in cur.fetchall():
                print(table[0], end=' ')
        print("\n[Note: This action is irreversible and you will lose all the data of this camp]")
        consent = input("Are you sure you want to de-register this camp?(y/n): ")

        if consent.lower() == 'y':
            cur.close()
            conn.close()
            cur,conn = connect()
            cur.execute("DROP DATABASE " + campName + ";")
            print("Successfully de-registered " + campName)
        else:
            print("Operation Aborted!")
        cur.close()
        conn.close()

def readRelation():
    """ Reads a database """
    inp = input("Enter the camp name: ")
    campName = "camp" + inp 
    # campName = inp        # uncomment this to access testingBase database and comment out above line

    # connect to default database
    cur, conn = connect()
    # list all databases
    cur.execute("SELECT datname FROM pg_database;")
    db_list = list()
    for db in cur.fetchall():
        db_list.append(db[0])
    
    if campName in db_list:
        cur.close()
        conn.close()
        
        # connect to required camp database
        cur, conn = connect(campName)
        # find all existing relations/tables in database
        cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
        
        if cur.rowcount == 0:
            print("NO relation found in " + campName)
        else:
            print("\nRelations of " + campName + " :")
            print("==> ", end ='')

            all_relations = list()
            # print all the relations in current database
            for table in cur.fetchall():
                # print(table)
                print(table[2], end=', ')        #prints the table name only
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


# def requestDetailModification():
#     """ sends a request to the camp associated with the database, so admin's can approve/disapprove the request for modification """
#     pass

def listAllCamps():
    """ Lists out the information of all camps registered """
    cur,conn = connect("all_camp_details")
    # year = input("Enter the year of which camps you want to access (yyyy): ")
    detailsOf = "campdet" + "2021"
    
    print("1. Print campNames only")
    print("2. Print all details of each camp")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print("All camps registered in 2021 are: ")
        cur.execute("select * from " + detailsOf + ";")
        for item in cur.fetchall():
            print(item[1],end = '\t')
        print()

    elif choice == 2:
        print("Details of all camps registered in year 2021: ")
        header = ["campId","campName","state","district","city_or_village","coordinates","Admin","Total Capacity","Capacity Full?"]
        for item in header:
            print(item,end='\t')
        print()
        
        cur.execute("select * from " + detailsOf + ";")
        for row in cur.fetchall():
            for item in row:
                print(item,end='\t')
            print()
    cur.close()
    conn.close()

''' -------- CampAdmin portal functions -------- '''
def readThis(campName):
    pass
    # Establish connection to database of the camp
    # cur,conn = connect(campName)

    # Will be implemented after write is implemented
    # because in order to read, we need the structure of write

def writeInto(campName):
    pass

def removeFrom(campName):
    pass

def directFrom(campName):
    pass

def findVacancies():
    pass

def requestReadSupply():
    pass

def requestGetSupply():
    pass

def readTodayAll():
    pass

def feedback():
    pass

def checkDonationStatus():
    pass


''' -------- Driver function -------- '''
if __name__ == '__main__':
    # cur = connect()
    
    which_portal = input("Select a portal (Camp-Admin (c)/System-Admin (s)): ")
    if which_portal.lower() == 's':
        pswd = input("Enter password to access System-Admin portal: ")
        # password check method (dummy)
        if pswd == "IamSysAdmin99":
            choice = -1
            while choice != 0:
                print("\n----------Welcome to Admin portal-----------")
                print("1. Register a camp")
                print("2. Deregister an accidentally registered camp")
                print("3. Read the relations of a camp")
                print("4. List all camps and their details")
                # print("4. Request detail modification of a camp's relation")
                print("0. Exit")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    registerCamp()
                elif choice == 2:
                    deRegister()
                elif choice == 3:
                    readRelation()
                elif choice == 4:
                    listAllCamps()
                elif choice == 0:
                    print("Exiting ...")
                    exit(0)
                else:
                    print("Error!! wrong choice")
        else:
            print("\nWrong Password, Access Denied!")
            exit(0)
    
    elif which_portal.lower() == 'c':
        campId = input("Enter your camp ID: ")
        campName = "camp"  + campId
        cur,conn = connect()
        cur.execute("SELECT datname from pg_database;")
        db_list = list()
        for db in cur.fetchall():
            db_list.append(db[0])
        
        cur.close()
        conn.close()

        if (campName) not in db_list:
            print("Error!! There's no camp with id " + campId)
            exit(-1)
        else:
            pswd = input("Enter password of camp" + campId + ": ")

            # password check (dummy)
            if pswd == "IamCampAdmin88":
                # NOTE: we will maintain whether a person is present in camp or left, 
                # so that even if person leaves, we have his/her information
                # new column char(1) Present? (y/n)

                # one more column containing Flood codename will be present
                # will be same for all people 
                # but when database used in another flood later
                # flood codename will be updated and will be same for all people coming then
                # so on

                # contains consolidated information of camp, location, id, authorities list
                # maintainers etc (in a file or a new relation)

                choice = -1
                while choice != 0:
                    # cur, conn = connect("camp"+campId)    # no need to connect here
                    print("\n----------Welcome to CampAdmin portal-----------") 
                    print("Connected to your camp camp" + campId + "\n")
                    print("1. Read Record(s)")
                    print("2. Enter a new Person's Record")
                    # This will first check if the camp is full or not => count(people) [technically count(tuples where Present='y')]
                    # if yes, call (5) or (6) and then (4) accordingly
                    # will also check if age > 60, should be taken to 60+ camps
                    # and < 60 should be kept in < 6o age camps
                    # according call (4)
                    # Also there would be date when this person entered in camp

                    print("3. Remove an existing Record")
                    # also a col containing LeftDate needs to be updated
                    print("4. Direct an Person to other camp (requires informing the other side)")
                    print("5. Find vacancies in nearby camps")
                    # print("6. Find vacancies in all camps")
                    print("6. Request read access to supply data/resources of other camp")
                    print("7. Request an emergency item/resource supply from other camp(s)")

                    print("8. Read new entries of the day in other camps")
                    # also allows search in today's new entries of other camps
                    # contains UniteProgram inside, so can unite the people who are found to their families
                    
                    print("9. Send Feedback to SysAdmin (to NDRF authorities)")
                    # from general feedback to all types, including education of students, requirements, etc
                    print("10. Check donation status")
                    print("0. Exit")
                    choice = input("Enter a choice: ")

                    if choice == 1:
                        readThis(campName)
                    elif choice == 2:
                        writeInto(campName)
                    elif choice == 3:
                        removeFrom(campName)
                    elif choice == 4:
                        directFrom(campName)
                    elif choice == 5:
                        findVacancies()
                    elif choice == 6:
                        requestReadSupply()
                    elif choice == 7:
                        requestGetSupply()
                    elif choice == 8:
                        readTodayAll()
                    elif choice == 9:
                        feedback()  # will have section-wise feedback
                    elif choice == 10:
                        checkDonationStatus()
                    elif choice == 0:
                        print("Exiting...")
                        exit(0)
                    else:
                        print("Error! Invalid choice.")
                        choice = 0
                        print("Exiting...")
                
                                    