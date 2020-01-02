#!/usr/bin/env bash

# Author: m8r0wn
# Script: setup.sh

# Description:
# enumdb setup script to verify all required packages
# are installed on the system.

#Check if Script run as root
if [[ $(id -u) != 0 ]]; then
	echo -e "\n[!] Setup script needs to run as root\n\n"
	exit 0
fi

echo -e "\n[*] Starting enumdb setup script"

apt-get update

echo -e "[*] Checking for Python 3"
if [[ $(python3 -V 2>&1) == *"not found"* ]]
then
    echo -e "[*] Installing Python3"
    apt-get install python3 -y
else
    echo "[+] Python3 installed"
fi

echo -e "[*] Checking for required enumdb libraries"
if [[ $(python3 -c "import MySQLdb" 2>&1) == *"No module"* ]]
then
    echo -e "[*] Installing python3-MySQLdb"
    apt-get install python3-mysqldb -y
else
    echo "[+] MySQLdb installed"
fi

if [[ $(python3 -c "import pymssql" 2>&1) == *"No module"* ]]
then
    echo -e "[*] Installing python3-pymssql"
    apt-get install python3-pymssql -y
else
    echo "[+] pymssql installed"
fi

if [[ $(python3 -c "import openpyxl" 2>&1) == *"No module"* ]]
then
    echo -e "[*] Installing python3-openpyxl"
    apt-get install python3-openpyxl -y
else
    echo "[+] openpyxl installed"
fi

if [[ $(python3 -c "import ipparser" 2>&1) == *"No module"* ]]
then
    echo -e "[*] Installing python3-ipparser"
    pip3 install ipparser
else
    echo "[+] ipparser installed"
fi

echo -e "\n[*] enumdb setup complete\n\n"