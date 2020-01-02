from sys import stdout

def print_success(msg):
    # Green
    stdout.write('\033[1;32m[+]\033[1;m {}\n'.format(msg))


def print_status(msg):
    # Blue
    stdout.write('\033[1;34m[*]\033[1;m {}\n'.format(msg))


def print_failure(msg):
    # Red
    stdout.write('\033[1;31m[-]\033[1;m {}\n'.format(msg))


def print_empty(msg):
    # Yellow
    stdout.write('\033[1;33m[-]\033[1;m {}\n'.format(msg))


def print_closing(msg):
    # White
    stdout.write('\033[1;37m[*]\033[1;m {}\n'.format(msg))