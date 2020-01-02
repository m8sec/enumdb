# enumdb
Enumdb is a brute force and post exploitation tool for MySQL and MSSQL databases. When provided a list of usernames and/or passwords, it will cycle through each targeted host looking for valid credentials. By default, enumdb will use newly discovered credentials to search for sensitive information in the host's databases via keyword searches on the table or column names. This information can then be extracted and reported to a .csv or .xlsx output file. See the Usage and All Options sections for more detailed usage and examples.

To make the tool more adaptable on larger environments, Threading has been added to expedite brute forcing and enumeration when targeting multiple servers. Additionally, enumdb will not generate a report by default allowing users to get a quick preview of the target database. To extract data, specify a report type in the command line arguments, with either: ```-r csv``` or ```-r xlsx```. The first 100 rows of each identified table or column will be selected in the output report. 

The number of rows captured in reports, blacklisted databases & tables, and keywords for table & column searches can be modified at the top of enumdb.py

## Installation
Kali Linux was designed and testing using Python3 on the Kali Linux operating system. However, backwards compatibility has recently been added for Python2.7.

*Use the requirements file to install the necessary Python packages. If you still experience import issues, try the setup.sh file*
```bash
git clone https://github.com/m8r0wn/enumdb
cd enumdb
pip3 install -r requirements.txt
``````

## Usage
* Connect to a MySQL database and search for data via key word in table name (no report)<br>
`python3 enumdb.py -u root -p '' -t mysql 10.11.1.30`

* Connect to a MSSQL database using a domain username and search for data via keyword in column name writing output to csv file:<br>
`python3 enumdb.py -u 'domain\\user' -p Winter2018! -t mssql -columns -report csv 10.11.1.30`

* Brute force multiple MySQL servers looking for default credentials, no data enumeration:<br>
`python3 enumdb.py -u root -p '' -t mysql -brute 10.11.1.0-30`

* Brute force MSSQL sa account login. Once valid credentials are found, enumerate data by column name writing output to xlsx:<br>
`python3 enumdb.py -u sa -P passwords.txt -t mssql -columns -report xlsx 192.168.10.10`

* Brute force MSSQL sa account on a single server, no data enumeration:<br>
`python3 enumdb.py -u sa -P passwords.txt -t mssql -brute 192.168.10.10`

![enumdb](https://user-images.githubusercontent.com/13889819/54823551-9ae80d00-4c7e-11e9-89e5-3140b793b6d7.gif)

## All Options
      -h, --help                show help message and exit
      -u USERS                  Single username
      -U USERS                  Users.txt file
      -p PASSWORDS              Single password
      -P PASSWORDS              Password.txt file
      -threads MAX_THREADS      Max threads (Default: 3)
      -port PORT                Specify non-standard port
      -r REPORT, -report REPORT Output Report: csv, xlsx (Default: None)
      -t DBTYPE                 Database types currently supported: mssql, mysql
      -c, -columns              Search for key words in column names (Default: table names)
      -v                        Show failed login notices & keyword matches with Empty data sets
      -brute                    Brute force only, do not enumerate


