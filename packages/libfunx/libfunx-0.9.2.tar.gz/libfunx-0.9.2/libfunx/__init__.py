"""LIBrary of utility FUNCtionS for catpdf minmon swapdf toc2md and wmtile"""

__version__ = "0.9.2"

# imports

from os import popen
from os.path import split as splitpath, join as joinpath, abspath, expanduser, isfile, isdir, islink, exists
from sys import argv, exit

# string functions

def take(string, allowed, default='', join_by=''):
    'take allowed chars from string and replace not allowed chars by default, joined by join_by'
    return join_by.join(char if char in allowed else default for char in string)

def drop(string, forbidden, default='', join_by=''):
    'drop forbidden chars from string and replace them by default, joined by join_by'
    return join_by.join(default if char in forbidden else char for char in string)

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

def shell_ask(question, answers="yn"):
    "return answer to question at terminal"
    while True:
        answer = input(f"{question} [{'/'.join(answers)}] --> ").strip()
        if answer in set(answers):
            return answer

def shell_lines(command):
    "perform shell command and return stdout as a list of notempty rstripped lines"
    return [line for line in [line.rstrip() for line in popen(command)] if line]

# sequence functions

def show(xx):
    "for x in xx: print(x)"
    for x in xx:
        print(x)

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

def get_source(source, ext=""):
    "check source file and return it as absolute path"
    source = abspath(expanduser(source))
    if not source.endswith(ext):
        exit(f"ERROR: source {source!r} doesn't end with {ext!r}")
    elif not exists(source):
        exit(f"ERROR: source {source!r} doesn't exist")
    elif not isfile(source):
        exit(f"ERROR: source {source!r} exists but is not first file")
    else:
        return source
        
def get_target(target, ext="", yes=False, no=False):
    "check target file and return it as absolute path"
    if yes and no:
        exit("ERROR: you can't give both -y and -n arguments")
    target = abspath(expanduser(target))
    if not target.endswith(ext):
        exit(f"ERROR: target {target!r} doesn't end with {ext!r}")
    elif exists(target):
        if not isfile(target):
            exit(f"ERROR: target {target!r} exists and is not first file")
        elif no or not yes and shell_ask(f"target file {target!r} exists, overwrite?") == "n":
            exit(f"target file {target!r} exists, not overwritten")
    return target

def show(lines):
    "for line in lines: print(line.rstrip())"
    for line in lines:
        print(line.rstrip())

def package_file(name):
    "get absolute path of file in package"
    return joinpath(splitpath(__file__)[0], name)

# various functions

def try_func(func, args, on_error=None):
    "try: return func(*args); except: return on_error"
    try:
        return func(*args)
    except:
        return on_error
