# 这个是我简单修改的 binpython 源码！！！注意先去克隆官方的 binpython 仓库再把这个文件复制到仓库里去！！！

#BINPython AGPL-V3.0 LICENSE Release
#Under the AGPL-V3 license
#full version


####################################
#build configure

ver = "0.46"
libs_warning = "1"
#1 is ture 0 is false.
#Changing the value to 0 will close the prompt that the library does not exist


releases_ver = "official"
importlibs = "" # For custom imported libraries before building, use "," to separate them (must be installed in the native Python before building), or directly use import <library> to add to the list below, example: importlibs = "os,sys,wget,flask"
cmdver = "0.08"

####################################

#BINPython function and variable START

class binpythoninfo:
    def ver():
        print(ver)

    def libs_warning():
        print(libs_warning)

    def releases_ver():
        print(releases_ver)

    def build_importlibs():
        print(importlibs)
from os import makedirs
import time
#get system info(windows or linux ...)
import platform
sys = platform.system()
#if system is windows, then enable setwindowtitle() function
if sys == "Windows":
    class binpythonwin:
        def setwindowtitle(titlename):
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(titlename)
#print binpython all configure function
def binpythonallconf():
    print("ver: " + ver + " buildversion: " + " libs_warning settings:" + libs_warning + " releases full version: " + releases_ver + " custom library that has been build: " + importlibs)
#if system is windows, show default window title
if sys == "Windows":
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW("BINPython for TaoLISystem Tools" + ver)
try:
    if importlibs != '':
        import importlib
        libraries = importlibs.split(",")
        for lib in libraries:
            importlib.import_module(lib)
#get libswarning
except ImportError as e:
    if libs_warning == "1":
        print("Warning: Custom import library %s does not exist, please check the source code library configuration and rebuild" % importlibs)
        print("Error: " + str(e))
        print("")
#run python files option(-f)
def optreadfile():
    import sys
    getfile = sys.argv[1]
    getfilecode = open(getfile,encoding = "utf-8")
    exec(getfilecode.read())
    sys.exit(0)

# 导入所需的库
import os
import re
import sys
import ctypes
import operator
import traceback
import shutil
import subprocess
import ast
import errno
import struct
import time
import serial
import serial.tools
import serial.tools.list_ports

#main BINPython
def binpython_welcome_text():
    print("BINPython for TaoLiSystem Tools " + ver + "-" + releases_ver + " Python " + platform.python_version() + " [Running on " + platform.platform() + " " + platform.version() + "]")
    print('Type "about", "help", "copyright", "credits" or "license" for more information. Type "binpython_cmd()" to enter BINPython CMD')
def binpython_shell():
    while True:
        try:
            pycmd=input(">>> ")
            if pycmd in globals().keys():
                print(globals()[pycmd])
                continue
            elif pycmd == 'about':
                print("BINPython By: Edward Hsing[https://github.com/xingyujie] AGPL-3.0 LICENSE Release")
            elif pycmd == 'help':
                print("Type help() for interactive help, or help(object) for help about object.")
            elif pycmd == 'copyright':
                print("""
Copyright (c) 2001-2022 Python Software Foundation.
All Rights Reserved.

Copyright (c) 2000 BeOpen.com.
All Rights Reserved.

Copyright (c) 1995-2001 Corporation for National Research Initiatives.
All Rights Reserved.

Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.
All Rights Reserved.
""")
            elif pycmd == 'credits':
                print("""
Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
    for supporting Python development.  See www.python.org for more information.
    """)
            elif pycmd == 'license':
                print("Type license() to see the full license text")
            elif pycmd == 'binpython_cmd':
                binpython_cmd()
            else:
                exec(pycmd)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            sys.exit()
        except Exception as err:
            print(err)
try:
    optreadfile()
except:
    pass


#def
#print all helpinfo
helpinfo = """
Usage: binpython [OPTIONS]

Options:
<filename>                         Enter a Python filepath and run the script (*.py) [or -f <filename>]
-h            --help               View this help documentation
-c            --cmd                BINPython CMD (Use the "help" command to view cmd help)
-v            --version            Print BINPython Version
"""

def custhelp():
    try:
        f = open("binpython_config/help.txt",encoding = "utf-8")
        print(f.read())
    except:
        print(helpinfo)
#set about info
about = "BINPython " + ver + "-" + releases_ver + " By: DigitalPlat Edward Hsing [https://github.com/xingyujie/binpython, http://digitalplat.org, http://binpython.org] AGPL-3.0 LICENSE Release"
#getopt
try:
    import getopt
#set options
    opts,args = getopt.getopt(sys.argv[1:],'-h-f:-c-v',['help','file=','cmd','version'])
#set getopt error prompt
except getopt.GetoptError as err:
    print("Please check help:")
    print("Invalid gargument. Please check help.")
#show full help(custhelp())
    custhelp()
    sys.exit()
#get every argv
for opt_name,opt_value in opts:
    def execpyfile(filename):
        f = open(filename)
        exec(f.read())
    if opt_name in ('-h','--help'):
#-h show full help function
        custhelp()
        sys.exit()
    if opt_name in ('-v','--version'):
#-v show version(read custom config)
        try:
            f = open("binpython_config/version.py",encoding = "utf-8")
            exec(f.read())
            print("Powered by: BINPython[https://github.com/xingyujie/binpython] AGPL 3.0")
        except:
            print("BINPython " + ver + "-" + releases_ver + " By: DigitalPlat Edward Hsing [https://github.com/xingyujie/binpython, http://digitalplat.org, http://binpython.org] AGPL-3.0 LICENSE Release")
            print("Python " + platform.python_version())
        sys.exit()
    if opt_name in ('-f','--file'):
#-f runfile(or no option)
        file = opt_value
        f = open(file,encoding = "utf-8")
        exec(f.read())
        sys.exit()

if len(sys.argv) == 1:
    binpython_welcome_text()
    binpython_shell()