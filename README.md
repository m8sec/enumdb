# enumdb
Enumdb is a brute force and post exploitation tool for MySQL and MSSQL databases. When provided a list of usernames and/or passwords, it will cycle through each targeted host looking for valid credentials. By default, enumdb will use newly discovered credentials to search for sensitive information in the host's databases via keyword searches on the table or column names. This information can then be extracted and reported to a .csv or .xlsx output file. See the Usage and All Options sections for more detialed usage and examples.

The latest version, enumdb v2.0, has been adapted for larger environments:
* Keyword searches can now be conducted on table or column names to identify sensitive information. These terms can be customized at the top of enumdb.py.
* Threading has been added to expedite brute forcing and enumeration on larger networks.
* Enumdb no longer generates reports by default. Reporting (csv/xlsx) must be defined in the command line arguments.
* When extracting data for reports, users can now define a limit on the number of rows selected. The default value of 100, can be modified at the top of enumdb.py.
* Enumdb's output formatting has been modified to provide more concise feedback when enumerating large amounts of data.

*Enumdb is written in python3 and tested on Kali Linux, use the setup.sh script to ensure all required libraries are installed.*

![](https://user-images.githubusercontent.com/13889819/35242124-ad8e3d9e-ff86-11e7-8f50-bfe2f20160cd.gif)

## Installation
```bash
git clone https://github.com/m8r0wn/enumdb
cd enumdb
pip3 install -r setup/requirements.txt
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

## All Options
    -u USERS              Single username
    -U USERS              Users.txt file
    -p PASSWORDS          Single password
    -P PASSWORDS          Password.txt file
    -threads MAX_THREADS  Max threads (Default: 3)
    -port PORT            Specify non-standard port
    -report REPORT        Output Report: csv, xlsx (Default: None)
    -t DBTYPE             Database types currently supported: mssql, mysql
    -columns              Search for key words in column names (Default: table names)
    -v                    Show keyword matches that respond with no data
    -brute                Brute force only, do not enumerate
