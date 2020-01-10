# enumdb
Enumdb is a brute force and post exploitation tool for MySQL and MSSQL databases. When provided a list of usernames and/or passwords, it will cycle through each targeted host looking for valid credentials. By default, enumdb will use newly discovered credentials to search for sensitive information in the host's databases via keyword searches on the table or column names. This information can then be extracted and reported to a .csv or .xlsx output file. See the Usage and All Options sections for more detailed usage and examples.

To make the tool more adaptable on larger environments, Threading has been added to expedite brute forcing and enumeration when targeting multiple servers. Additionally, enumdb will *not* generate reports by default, allowing users to get a quick preview of the target database. To extract data, specify a report type in the command line arguments, with either: ```-r csv``` or ```-r xlsx```. The first 100 rows of each identified table or column will be extracted in the output report. 

Rows captured, blacklisted databases & tables, and keywords searches can all be modified at: ```enumdb/config.py```.

## Installation
Enumdb was designed and tested using Python3 for Debian based Linux systems. However, the tool is also compatible with Python2.7, and on other Linux distributions.

```bash
git clone https://github.com/m8r0wn/enumdb
cd enumdb
python3 setup.py install
``````

If experiencing issues with the [MySQLdb](https://github.com/PyMySQL/mysqlclient-python), additional MySQL development resources may
need to be installed:

* Debian / Ubuntu: 
```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

* Red Hat / CentOS: 
```
sudo yum install python3-devel mysql-devel
```

## Usage
* Connect to a MySQL database and search for data via key word in table name (no report)<br>
```enumdb -u root -p '' -t mysql 10.11.1.30```

* Connect to a MSSQL database using a domain username and search for data via keyword in column name writing output to csv file:<br>
```enumdb -u 'domain\\user' -p Winter2018! -t mssql -columns -report csv 10.11.1.30```

* Brute force multiple MySQL servers looking for default credentials, no data enumeration:<br>
```enumdb -u root -p '' -t mysql -brute 10.11.1.0-30```

* Brute force MSSQL sa account login. Once valid credentials are found, enumerate data by column name writing output to xlsx:<br>
```enumdb -u sa -P passwords.txt -t mssql -columns -report xlsx 192.168.10.10```

* Brute force MSSQL sa account on a single server, no data enumeration:<br>
```enumdb -u sa -P passwords.txt -t mssql -brute 192.168.10.10```

![enumdb](https://user-images.githubusercontent.com/13889819/54823551-9ae80d00-4c7e-11e9-89e5-3140b793b6d7.gif)

## All Options
```html
  -u USERS                  Single username
  -U USERS                  Users.txt file
  -p PASSWORDS              Single password
  -P PASSWORDS              Password.txt file
  -threads MAX_THREADS      Max threads (Default: 3)
  -port PORT                Specify non-standard port
  -r REPORT, -report REPORT Output Report: csv, xlsx (Default: None)
  -t {mysql,mssql}          Database type
  -c, -columns              Search for key words in column names (Default: table names)
  -v                        Show failed login notices & keyword matches with Empty data sets
  -brute                    Brute force only, do not enumerate

```