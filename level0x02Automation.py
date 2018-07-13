import os
import sys
import subprocess
import config

def installGo():
    try:
        print("\033[1;32m[+]Downloading Go Package\033[1;m")
        proc = subprocess.Popen(config.goDownloadCommand, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        print(output)
        print("\033[1;32m[+]Unzipping Go Package\033[1;m")
        proc = subprocess.Popen(config.unzipGoPackage, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        print(output)
        proc = subprocess.Popen(config.moveGoPackageToSystem, stdout=subprocess.PIPE,shell=True)
        output = proc.stdout.read()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to install Go\033[1;m" + str(e)
        sys.exit()











#1. Check if Go is installed, if not install Go
proc = subprocess.Popen('go version', stdout=subprocess.PIPE, shell=True)
output = proc.stdout.read()
isGoInstalled = False
if output == "":
    isGoInstalled = False
    print "\033[1;32m[+]Installing Go language\033[1;m"
    #Call function to install go
    try:
        installGo()
        isGoInstalled = True
    except Exception as e:
        print e
else:
    print "\033[1;32m[+]Found Go language\033[1;m"
    isGoInstalled = True
print(isGoInstalled)

#2. Check if subfinder is installed, else install it