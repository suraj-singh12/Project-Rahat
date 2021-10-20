from config import config

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Database:
    def validate(self, usrType, identity, pswd):
        ''' used to validate password;    usrType: sys_admin/camp_admin, identity: campName/"sysadmin"  pswd: password '''
        
        # read passwords file (this file is on server)
        params = config("passwords.ini",usrType)
        # fetch password of given identity
        ac_pass = params.get(identity)

        if ac_pass is not None and  pswd == ac_pass:
            return True
        return False

    def connect(self, database=''):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            # if a database is specified during connection, then connect to that otherwise default
            if database != '':      
                params['database'] = database
            conn = psycopg2.connect(**params)

            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            # enabled isolation_level_autocommit ; now databases can be created without issue
            # print("Connected successfully.\n")

            # create a cursor
            cur = conn.cursor()
            return cur,conn

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def listAllDatabases(self, cur):
        # list all databases
        cur.execute("SELECT datname FROM pg_database;")
        db_list = list()
        for db in cur.fetchall():
            db_list.append(db[0])
        return db_list

    def isPresentCamp(self, database):
        # connect to default database
        cur, conn = self.connect()
        # list all databases present in system (i.e. all registered camps)
        db_list = self.listAllDatabases(cur)
        # close cursor and connection with default database
        cur.close()
        conn.close()

        # check the presence of database in all databases
        if database in db_list:
            return True
        return False
