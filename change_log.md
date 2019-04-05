### Change Log

#### v.2.0.7
* Implement IPParser module to extract host information from cmd args

#### v.2.0.6
* Python 2.7 backwards compatibility
* If run without a password, enumdb will prompt for a password at runtime. This removes the value from being saved in .bash_history. 
* Minor code updates

#### v2.0.5
* Keyword searches can now be conducted on table or column names to identify sensitive information. These terms can be customized at the top of enumdb.py.
* Threading has been added to expedite brute forcing and enumeration on larger networks.
* Enumdb no longer generates reports by default. Reporting (csv/xlsx) must be defined in the command line arguments.
* When extracting data for reports, users can now define a limit on the number of rows selected. The default value of 100, can be modified at the top of enumdb.py.
* Enumdb's output formatting has been modified to provide more concise feedback when enumerating large amounts of data.