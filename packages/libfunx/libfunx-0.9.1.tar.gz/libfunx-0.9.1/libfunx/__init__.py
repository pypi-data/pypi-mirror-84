"""LIBrary of utility FUNCtionS for catpdf minmon swapdf toc2md and wmtile"""

__version__ = "0.9.1"

# imports

from os import popen
from os.path import split as splitpath, join as joinpath, abspath, expanduser, isfile, isdir, islink, exists
from sys import argv, exit

# string functions

def take(string, allowed, default='', joinby=''):
    'take allowed chars from string and replace not allowed chars by default'
    return joinby.join(char if char in allowed else default for char in string)

def drop(string, forbidden, default='', joinby=''):
    'drop forbidden chars from string and replace them by default'
    return joinby.join(default if char in forbidden else char for char in string)

def no_html_tags(string):
    "remove HTML tags '<...>' from string"
    result = ""; tag = False
    for char in string:
        if char == "<":
            tag = True
        if not tag:
            result += char
        if char == ">":
            tag = False
    return result

# shell functions

def shell_lines(command):
    "perform shell command and return stdout as a list of notempty rstripped lines"
    return [line for line in [line.rstrip() for line in popen(command)] if line]

# sequence functions

def show(lines):
    "for line in lines: print(line)"
    for line in lines:
        print(line)

def find_in(xx, yy):
    "find first j such that xx[j] in yy, -1 if not found"
    for j, xj in enumerate(xx):
        if xj in yy:
            return j
    else:
        return -1

def find_not_in(xx, yy):
    "find first j such that xx[j] not in yy, -1 if not found"
    for j, xj in enumerate(xx):
        if xj not in yy:
            return j
    else:
        return -1

def rfind_in(xx, yy):
    "find last j such that xx[j] in yy, -1 if not found"
    for j in range(len(xx) - 1, -1, -1):
        if x[j] in yy:
            return j
    else:
        return -1

def rfind_not_in(xx, yy):
    "find last j such that xx[j] not in yy, -1 if not found"
    for j in range(len(xx) - 1, -1, -1):
        if x[j] not in yy:
            return j
    else:
        return -1

# file functions

def package_file(name):
    "get absolute path of file in package"
    return joinpath(splitpath(__file__)[0], name)
