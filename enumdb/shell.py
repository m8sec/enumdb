from enumdb.printers import *

class DBShell():
    def __init__(self, db_class, host, port, user, passwd):
        self.db = db_class
        self.con = self.db.connect(host, int(port), user, passwd, verbose=False)
        if self.con:
            self.cmd_loop()

    def cmd_loop(self):
        help = "\n\t\tEnumDB Shell\n\n"
        help += "help                             - Show help menu\n"
        help += "edb_databases                    - list all databases\n"
        help += "edb_tables [DB]                  - list tables in DB\n"
        help += "edb_columns [table].[DB]         - list columns in table\n"
        help += "edb_dump [table].[DB] [#rows]    - Get data from table\n"
        help += "[SQL Query]                      - Execute raw SQL query\n"

        while True:
            try:
                self.output = []
                cmd = input("\nenumdb#> ")
                cmd = cmd.lstrip().rstrip()

                if cmd == 'exit':
                    try:
                        print('Closing database connection...')
                        self.con.close()
                    except:
                        pass
                    return True

                elif cmd == 'help':
                    print(help)

                elif cmd == 'edb_databases':
                    for x in self.db.get_databases(self.con):
                        print(x)

                elif cmd.startswith('edb_tables'):
                    database = cmd.split(" ")[-1]
                    for x in self.db.get_tables(self.con, database):
                        print(x)

                elif cmd.startswith('edb_columns'):
                    table, database = cmd.split(" ")[-1].split(".")
                    for x in self.db.get_columns(self.con, database, table):
                        print(x)

                elif cmd.startswith('edb_dump'):
                    s = cmd.split(" ")
                    table, database = s[1].split(".")
                    # Validate row input (select count)
                    try:
                        rows = s[-1]
                        if int(rows) < 0:
                            raise Exception()
                    except:
                        print_status("Invalid row value, using default (10)")
                        rows = 10
                    for x in self.db.get_data(self.con, database, table, rows):
                        print(x)

                else:
                    for x in self.db.db_query(self.con, cmd):
                        print(x)

            except Exception as e:
                print("enumdb Err: {}".format(str(e)))