Help on package libfunx:
```
NAME

    libfunx - LIBrary of utility FUNCtionS for catpdf minmon swapdf toc2md and wmtile

PACKAGE CONTENTS

FUNCTIONS

    ask(question, answers='yn')
        return answer to question at terminal
    
    drop(string, forbidden, default='', join_by='')
        drop forbidden chars from string and replace them by default, joined by join_by
    
    exit(status=None, /)
        Exit the interpreter by raising SystemExit(status).
        
        If the status is omitted or None, it defaults to zero (i.e., success).
        If the status is an integer, it will be used as the system exit status.
        If it is another kind of object, it will be printed and the system
        exit status will be one (i.e., failure).
    
    find(xx, y)
        find first j such that xx[j] == y, -1 if not found
    
    find_in(xx, yy)
        find first j such that xx[j] in yy, -1 if not found
    
    find_not_in(xx, yy)
        find first j such that xx[j] not in yy, -1 if not found
    
    get_source(source, ext='')
        check source file and return it as absolute path
    
    get_target(target, ext='', yes=False, no=False)
        check target file and return it as absolute path
    
    no_html_tags(string)
        remove HTML tags '<...>' from string
    
    package_file(name)
        get absolute path of file in package
    
    rfind(xx, y)
        find last j such that xx[j] == y, -1 if not found
    
    rfind_in(xx, yy)
        find last j such that xx[j] in yy, -1 if not found
    
    rfind_not_in(xx, yy)
        find last j such that xx[j] not in yy, -1 if not found
    
    shell(command)
        perform shell command and return stdout as a list of notempty rstripped lines
    
    show(xx)
        for x in xx: print(x)
    
    take(string, allowed, default='', join_by='')
        take allowed chars from string and replace not allowed chars by default, joined by join_by
    
    try_func(func, args, on_error=None)
        try: return func(*args); except: return on_error

DATA

    argv = ['./help.py']

VERSION

    0.9.3

FILE

    /home/xxxx/Documents/venv/libfunx/libfunx/libfunx/__init__.py
```


