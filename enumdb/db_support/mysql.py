import MySQLdb
from enumdb.printers import *
from enumdb.config import SELECT_LIMIT

class MySQL():
    def connect(self, host, port, user, passwd, verbose):
        try:
            con = MySQLdb.connect(host=host, port=port, user=user, password=passwd, connect_timeout=3)
            con.query_timeout = 15
            print_success("Connection established {}:{}@{}".format(user, passwd, host))
            return con
        except Exception as e:
            if verbose:
                print_failure("Login failed {}:{}@{}\t({})".format(user, passwd, host, e))
            else:
                print_failure("Login failed {}:{}@{}".format(user, passwd, host))
            return False

    def db_query(self, con, cmd):
        try:
            cur = con.cursor()
            cur.execute(cmd)
            data = cur.fetchall()
            cur.close()
        except:
            data = ''
        return data

    def get_databases(self, con):
        databases = []
        for x in self.db_query(con, 'SHOW DATABASES;'):
            databases.append(x[0])
        return databases

    def get_tables(self, con, database):
        tables = []
        self.db_query(con, "USE {}".format(database))
        for x in self.db_query(con, 'SHOW TABLES;'):
            tables.append(x[0])
        return tables

    def get_columns(self, con, database, table):
        # database var not used but kept to support mssql
        columns = []
        for x in self.db_query(con, 'SHOW COLUMNS FROM {}'.format(table)):
            columns.append(x[0])
        return columns

    def get_data(self, con, database, table):
        # database var not used but kept to support mssql
        return self.db_query(con, 'SELECT * FROM {} LIMIT {}'.format(table, SELECT_LIMIT))