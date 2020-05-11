import pymssql
from enumdb.printers import *
from enumdb.config import SELECT_LIMIT

class MSSQL():
    def connect(self, host, port, user, passwd, verbose=False):
        try:
            con = pymssql.connect(server=host, port=port, user=user, password=passwd, login_timeout=3, timeout=15)
            print_success("Connection established {}:{}@{}".format(user, passwd, host))
            return con
        except Exception as e:
            if verbose:
                print_failure("Login failed {}:{}@{}\t({})".format(user, passwd, host, e))
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
        for x in self.db_query(con, 'SELECT NAME FROM sys.Databases;'):
            databases.append(x[0])
        return databases

    def get_tables(self, con, database):
        tables = []
        for x in self.db_query(con, 'SELECT NAME FROM {}.sys.tables;'.format(database)):
            tables.append(x[0])
        return tables

    def get_columns(self, con, database, table):
        columns = []
        for x in self.db_query(con, 'USE {};SELECT column_name FROM information_schema.columns WHERE table_name = \'{}\';'.format(database, table)):
            columns.append(x[0])
        return columns

    def get_data(self, con, database, table, rows=False):
        # added row var for shell functionality
        if rows:
            select_limit = rows
        else:
            select_limit = SELECT_LIMIT
        self.db_query(con, "USE {}".format(database))
        return self.db_query(con, 'SELECT TOP({}) * FROM {}.dbo.{};'.format(select_limit, database, table))