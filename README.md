# enumdb
Enumdb is brute force and post exploitation tool for MySQL and MSSQL databases. When provided a list of usernames and/or passwords, it will cycle through each looking for valid credentials.

By default enumdb will use newly found, or given, credentials to search the database and find tables containing sensitive information (usernames, passwords, ssn, credit cards, etc), taking the manual work out of post exploitation. The data will be copied to a .xlsx output file in the current directory, listing one table per sheet. This output file can be changed to .csv using the command line arguments. Enumdb now supports targeting multiple servers. If using without the "-brute" option to enumerate the database, one file will be created for each server.

*Enumdb is written in python3, use the setup.sh script to ensure all required libraries are installed.*

![](https://user-images.githubusercontent.com/13889819/35242124-ad8e3d9e-ff86-11e7-8f50-bfe2f20160cd.gif)

## Getting Started
In the Linux terminal run:
1. git clone https://github.com/m8r0wn/enumdb
2. sudo chmod +x enumdb/setup.sh
3. sudo ./enumdb/setup.sh

## Usage
* Connect to a MySQL database and enumerate tables writing output to xlsx file:<br>
`python3 enumdb.py -u root -p '' -t mysql 10.11.1.30`

* Connect to a MSSQL database using a domain username and enumerate tables writing output to csv file:<br>
`python3 enumdb.py -u 'domain\\user' -p Winter2018! -t mysql -csv 10.11.1.30`

* Brute force multiple MySQL servers looking for default credentials:<br>
`python3 enumdb.py -u root -p '' -t mysql 10.11.1.0-30`

* Brute force MSSQL sa account login. Once valid credentials are found, enumerate data writing output to xlsx:<br>
`python3 enumdb.py -u sa -P passwords.txt -t mssql 192.168.10.10`

* Brute force MSSQL sa account login without enumerating data or logging output:<br>
`python3 enumdb.py -u sa -P passwords.txt -t mssql -brute 192.168.10.10`

## All Options
      -h, --help   show help message and exit
      -u USERS     Single username, OR
      -U USERS     Users.txt file
      -p PASSWORD  Single password, OR
      -P PASSWORD  Password.txt file
      -t DBTYPE    Database types: mssql, mysql
      -port PORT   Specify Non-standard port
      -csv         CSV output file (Default: xlsx)
      -brute       Brute force only, do not enumerate
