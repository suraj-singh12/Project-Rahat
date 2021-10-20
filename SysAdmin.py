from Database import Database

class SysAdmin(Database):
    ''' -------- System Admin portal functions -------- '''
    
    usrType = "sys_admin"
    identity = "sysadmin"

    def __init__(self, pswd):
        if not self.validate(SysAdmin.usrType, SysAdmin.identity, pswd):
            print("Authentication Failed !")
            exit(-1)


    def registerCamp(self):
        """ in technical terms: Creates a new database for a new camp """
        
        inp = input("Enter camp ID: ").lower()
        campName = "camp" + inp
        
        if self.isPresentCamp(campName):
            # connect to default database
            cur,conn = self.connect()

            # create database campName
            createDatabase = "CREATE DATABASE " + campName + ";"
            cur.execute(createDatabase)
            
            print("Camp " + campName + " successfully registered.")
            cur.close()
            conn.close()
        else:
            print("Camp " + campName + " already exists!!")
        

    def deRegister(self):
        """ in technical terms: drop a database"""
        
        inp = input("Enter camp ID: ").lower()
        campName = "camp" + inp

        if self.isPresentCamp(campName):
            # https://stackoverflow.com/questions/13719674/change-database-postgresql-in-python-using-psycopg2-dynamically

            # connect to required camp database
            cur,conn = self.connect(campName)
            # find all existing relations/tables in database
            cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
                
            if cur.rowcount == 0:
                print("No relation found in " + campName)
                cur.close()
                conn.close()
                return
            else:
                print("All these relations exist in " + campName + " :")
                for table in cur.fetchall():
                    print(table[0], end=' ')
                
                print("\n[Note: This action is irreversible and you will lose all the data of this camp]")
                consent = input("Are you sure you want to de-register this camp?(y/n): ")

                if consent.lower() == 'y':
                    # close connection with current database
                    cur.close()
                    conn.close()
                    # connect to default database
                    cur,conn = self.connect()
                    # drop the desired database
                    cur.execute("DROP DATABASE " + campName + ";")
                    print("Successfully de-registered " + campName)
                else:
                    print("Operation Aborted!")            
                # close connection with whatever database is connected
                cur.close()
                conn.close()


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


    def listAllRegCampsInfo(self):
        """ Lists out the information of all registered camps by specific year """
        
        cur,conn = self.connect("all_camp_details")

        year = input("Enter the year of which camps you want to access (yyyy): ")
        while (len(year) != 4) or (year.isnumeric() == False) or (year[0:3] != "202"):
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

            # printing campnames
            for item in cur.fetchall():
                print(item[1],end = '\t')
            print()

        elif choice == 2:
            print("Details of all camps registered in year 2021: ")
            header = ["campId","campName","state","district","city_or_village","coordinates","Admin","Admin_Aadhar","Total Capacity","Capacity Full?"]
            for item in header:
                print(item,end='\t')
            print()
            
            cur.execute("select * from " + tableName + ";")
            # printing details of all camps of entered year
            for row in cur.fetchall():
                for item in row:
                    print(item,end='\t')
                print()
        
        elif choice == 3:
            print("All camps registered in year 2021 are: ")
            cur.execute("select * from " + tableName + ";")
            camps = []
            for item in cur.fetchall():
                camps.append(item[1])
                print(item[1],end=', ')
            print()

            myCamp = input("Enter the camp Name: ")
            if myCamp not in camps:
                print("Error, no such camp exists !")
                return
            else:
                """ print the details of the camp with details of support members too """
                
                print()
                header = ["campId","campName","state","district","city_or_village","coordinates","Admin","Admin_Aadhar","Total Capacity","Capacity Full?"]
                for item in header:
                    print(item,end='\t')
                print()

                idd = myCamp[4:]
                # find details of current camp
                cur.execute("select * from " + tableName + " where campId = '" + idd + "' ;")
                # print details of this camp
                for row in cur.fetchall():
                    for item in row:
                        print(item,end='\t')
                    print()

                print()

                # print details of support members
                header = ["Member Name", "Member Aadhar"]
                print(header[0], '\t', header[1])
                
                cur.execute("select * from support_members2021 where campId = '" + idd + "';")
                for row in cur.fetchall():
                    for item in row[1:]:
                        print(item,end='\t')
                    print()
                print()
        else:
            print("Invalid Choice !")
        
        cur.close()
        conn.close()
