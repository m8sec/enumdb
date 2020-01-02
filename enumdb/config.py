# Key terms in table name to search for (all lowercase)
TABLE_KEY_WORDS = ['user', 'login', 'logon', 'config', 'hr', 'finance', 'account', 'password',
                   'passwd', 'hash', 'ssn', 'credit', 'social', '401k', 'benefits', 'pwd']

# Key terms in column name to search for (all lowercase)
COLUMN_KEY_WORDS = ['login', 'account', 'pass', 'ssn', 'credit', 'social', 'pwd']

# Database backlist, ex. information_schema (all lowercase)
DB_BLACKLIST = []

# Table backlist to skip (all lowercase)
TABLE_BLACKLIST = []

# Limit number of results in database dump
SELECT_LIMIT = 100