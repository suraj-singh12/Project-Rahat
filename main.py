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

import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # enabled isolation_level_autocommit ; now databases can be created without issue

        print("Connected successfully.")
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
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')

def registerCamp():
    """ in technical terms: Creates a new database for a new camp """
    inp = input("Enter camp ID: ").lower()
    campName = "camp" + inp
    
    # connect to database
    cur = connect()
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
        print("camp already exists!!")

def readRelation():
    """ Reads a database """
    pass

def requestDetailModification():
    """ sends a request to the camp associated with the database, so admin's can approve/disapprove the request for modification """
    pass

if __name__ == '__main__':
    # cur = connect()
    
    print("\n----------Welcome to Admin portal-----------")
    print("1. Register a camp")
    print("2. Read the relations of a camp")
    print("3. Request detail modification of a camp's relation")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        registerCamp()
    elif choice == 2:
        readRelation()
    elif choice == 3:
        requestDetailModification()
    else:
        print("Error!! wrong choice")
    