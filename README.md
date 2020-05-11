# enumdb
Enumdb is a relational database brute force and post exploitation tool for MySQL and MSSQL. When provided a list of usernames and/or passwords, it will cycle through each host looking for valid credentials. By default, enumdb will use newly discovered credentials to automatically search for sensitive data fields via keyword searches on table or column names. This information can then be extracted and reported to a .csv or .xlsx output file.

**Recent Additions:**
* Ability to spawn simulated shell on target, execute edb or custom SQL queries.
* Added threading during standard enumeration and brute force for faster results.
* No report by default, ```-r csv``` or ```-r xlsx``` required for data extraction.
* Failed login attempts will not be shown by default (```-v``` required).

*Number of rows extracted, blacklisted databases & tables, and keywords searches can all be modified at: ```enumdb/config.py```.*

## Installation
Enumdb was designed and tested using Python3 on Debian based Linux systems (kali). However, the tool is also compatible with Python2.7, and on other Linux distributions.
* PyPi (last release)
```bash
pip3 install enumdb
``````
* Or, GitHub (latest code)
```bash
git clone https://github.com/m8r0wn/enumdb
cd enumdb
python3 setup.py install
``````

## Usage
* Connect to a MySQL database and search for keywords in table names (no report)<br>
```enumdb -u root -p 'password123' -t mysql 10.11.1.30```

* Connect to a MSSQL database using domain credentials, search for data using keywords in column names, and extract to a .xlsx report:<br>
```enumdb -u 'domain\\user' -p Winter2018! -t mssql -columns -report xlsx 10.11.1.30```

* Brute force multiple MySQL servers looking for default credentials (no data or table enumeration)<br>
```enumdb -u root -p '' -t mysql --brute 10.11.1.0-30```

* Brute force MSSQL sa account login. Once valid credentials are found, enumerate data by table name writing output to a .csv report:<br>
```enumdb -u sa -P passwords.txt -t mssql -columns -report xlsx 192.168.10.10```

* Spawn an SQL shell on the system:<br>
```enumdb -u sa -P 'P@ssword1' -t mssql --shell 192.168.10.10```

<!--![enumdb](https://user-images.githubusercontent.com/13889819/54823551-9ae80d00-4c7e-11e9-89e5-3140b793b6d7.gif)-->

## All Options
```html
optional arguments:
  -h, --help          show this help message and exit
  -T MAX_THREADS      Max threads (Default: 10)
  -v                  Verbose output

Connection:
  -port PORT          Specify non-standard port
  -t {mysql,mssql}    Database type
  target              Target database server(s) [Positional]

Authentication:
  -u USERS            Single username
  -U USERS            Users.txt file
  -p PASSWORDS        Single password
  -P PASSWORDS        Password.txt file

Enumeration:
  -c, --columns       Search for key words in column names (Default: table names)
  -r {none,csv,xlsx}  Extract data and create output report

Additional Actions:
  --brute             Brute force only (No DB Enumeration)
  --shell             Launch SQL Shell
```

## Shell Commands
```
enumdb#> help
...
edb_databases                    - list all databases
edb_tables [DB]                  - list tables in DB
edb_columns [table].[DB]         - list columns in table
edb_dump [table].[DB] [#rows]    - Get data from table
[SQL Query]                      - Execute raw SQL query
```

## Troubleshooting
If experiencing issues with [MySQLdb](https://github.com/PyMySQL/mysqlclient-python), additional MySQL development resources may be required:

* Debian / Ubuntu: 
```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

* Red Hat / CentOS: 
```
sudo yum install python3-devel mysql-devel
```