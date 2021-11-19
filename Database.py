from config import config

import psycopg2
# important to import and enable isolation_level_autocommit otherwise database creation fails
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database:
    @staticmethod
    def validate(usrType, identity, pswd):
        """ used to validate password;
        usrType: sys_admin/camp_admin, identity: campName/"sysadmin"  pswd: password """

        # read passwords file (this file is on server)
        params = config("passwords.ini", usrType)
        # fetch password of given identity
        ac_pass = params.get(identity)

        if ac_pass is not None and pswd == ac_pass:
            return True
        return False

    @staticmethod
    def connect(database=''):
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
            # enabled isolation_level_autocommit; now databases can be created without issue
            # print("Connected successfully.\n")

            # create a cursor
            cur = conn.cursor()
            return cur, conn

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def listAllDatabases(self):
        print("Entered in listAllDatabases")
        # connect to default database
        cur, conn = self.connect()
        # query to list all databases
        cur.execute("SELECT datname FROM pg_database;")
        db_list = list()
        for db in cur.fetchall():
            db_list.append(db[0])
        cur.close()
        conn.close()
        print("db_list created")
        return db_list

    def isPresentCamp(self, database):
        # list all databases present in system (i.e. all registered camps)
        db_list = self.listAllDatabases()
        # check the presence of database in all databases
        if database in db_list:
            return True
        return False

    def readTable(self, database: str, table_name: str) -> tuple:
        """ reads a table and returns its data """

        # no need to authorize, as only authorized function from app will call it
        cur, conn = self.connect(database)
        cur.execute("SELECT * FROM " + table_name)
        data = list()

        for row in cur.fetchall():
            data.append(row)
        cur.close()
        conn.close()
        return tuple(data)
