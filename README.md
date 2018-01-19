# enumdb
Enumdb is brute force and post exploitation tool for MySQL and MSSQL databases. If provided a list of usernames and/or passwords, it will cycle through each looking for valid credentials.

By default enumdb will use newly found, or given, credentials to look through the database and find tables containing sensitive information (users, passwords, ssn, credit cards, etc). The data will be copied to a .xlsx output file for further evaluation. This output file can be changed to .csv using the command line arguments.

Enumdb is written in python3, use the setup.sh script to ensure all required libraries are installed.

## Getting Started
In the Linux terminal type:
* git clone https://github.com/m8r0wn/enumdb
* sudo chmod +x enumdb/setup.sh
* sudo ./enumdb/setup.sh

## Usage
Connect to a MySQL database and enumerate tables writing output to xlsx:<br>
`python3 enumdb.py -u root -p '' -t mysql 10.11.1.30`

Connect to a MSSQL database using a domain username and enumerate tables writing output to xlsx:<br>
`python3 enumdb.py -u 'domain\\user' -p Winter2018 -t mysql 10.11.1.30`

Connect to MySQL database and enumerate tables writing output to csv:<br>
`python3 enumdb.py -u root -p SecretPass! -t mysql -csv 10.0.0.1`

Brute force MSSQL sa account login. Once valid credentials are found, enumerate data writing output to xlsx:<br>
`python3 enumdb.py -u sa -P passwords.txt -t mssql 192.168.10.10`

Brute force MSSQL sa account login without enumerating data or logging output:<br>
`python3 enumdb.py -u sa -P passwords.txt -t mssql -brute 192.168.10.10`

## All Options
        -u          Username value
        -U          user.txt file

        -p          Password value
        -P          Pass.txt file

        -t         Database type: mssql, mysql
        -port      Specify Non-standard port

        -brute     Brute force only, do not enumerate
        -csv       CSV output file (default: xlsx)