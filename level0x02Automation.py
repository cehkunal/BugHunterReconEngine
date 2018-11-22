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

def setGoPath():
    try:
        proc = subprocess.Popen(config.setGoPath, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        print(output)
    except Exception as e:
        print "\033[1;31m[-]Exception: Error in setting GO Path\033[1;m" + str(e)

def removeGoPackages():
    try:
        proc = subprocess.Popen(config.removeGoPackage, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
        print(output)
    except Exception as e:
        print "\033[1;31m[-]Exception: Error in removing packages\033[1;m" + str(e)

def setGoBuildPath():
    try:
        proc = subprocess.Popen(config.setGoBuildPath, stdout=subprocess.PIPE, shell=True)
        output = proc.stdout.read()
    except Exception as e:
        print "\033[1;31m[-]Exception: Error in setting GO Build Directory Path\033[1;m" + str(e)

def installSubfinder():
    try:
        proc = subprocess.Popen(config.subfinderDownloadAndBuildCommand, stdout=subprocess.PIPE, shell = True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to install Subfinder\033[1;m" + str(e)
        sys.exit()

#TODO def setupSubFinderAPIKeys():

def subfinderScan(target):
    setGoPath()
    print "\033[1;32m[+]Finding subdomains with SUBFINDER\033[1;m"
    dirpath = os.getcwd()
    dest = target + ".subfinder "
    username = str(subprocess.Popen('echo $USER', stdout=subprocess.PIPE, shell=True).stdout.read()).strip()
    cmdList=[]
    if "root" not in username:
        cmdList = ['/home/',username, '/','go/bin/subfinder']
    else:
        cmdList = ['/root/','go/bin/subfinder']
    baseDir = ''.join(cmdList)
    cmd = baseDir + " -o " + dest + "-d " + target
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
    print "\033[1;32m[+]List of subdomains saved in " + dest + "\033[1;m"
    #output = proc.stdout.read()
    #TODO Change saved location and notify

def downloadMassDns():
    print "\033[1;32m[+]Downloading Massdns\033[1;m"
    try:
        proc = subprocess.Popen(config.downloadMassDns, stdout=subprocess.PIPE, shell=True).wait()
	if proc != 0:
		return
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to install MassDNS\033[1;m" + str(e)
    #Now, compile MassDNS
    print "\033[1;32m[+]Make Massdns\033[1;m"
    try:
        proc = subprocess.Popen(config.compileMassDns, stdout=subprocess.PIPE, shell=True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to Make MassDNS\033[1;m" + str(e)

def performMasscan(target):
    print "\033[1;32m[+]Initiating Massdns\033[1;m"
    cmd = './massdns/bin/massdns '+target+ '.subfinder'  +' -r  ./massdns/lists/resolvers.txt  -o S -w ' + target + '.massdns'
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True).wait()
    print "\033[1;32m[+]MASSDNS completed\033[1;m"

def filterMasscanresults(target):
    print "\033[1;32m[+]Filtering Massdns Results\033[1;m"
    file = target + ".massdns"
    f = open(file,"r")
    massdnsFiltered = []
    for line in f.readlines():
        if " A " in line:
            massdnsFiltered.append(line)
    f.close()
    writeFile = target + ".massdns.filtered"
    f = open(writeFile, "w")
    for line in massdnsFiltered:
        f.write(line)
    f.close()
    print "\033[1;32m[+]filtered Massdns Results\033[1;m"

def createIPListFromMassDnsFilteredList(target):
    print "\033[1;32m[+]Creating IP Space\033[1;m"
    filename = target + ".massdns.filtered"
    f = open(filename,"r")
    ipList = []
    for line in f.readlines():
        ip = line[line.index(' A ')+3:-1]
        ipStr = ip + "\n"
        ipList.append(ipStr)
    f.close()
    writeFileName = target + ".ipList"
    f = open(writeFileName,"w")
    for line in ipList:
        f.write(line)
    f.close()
    print "\033[1;32m[+]IP Space created\033[1;m"

def downloadMasscan():
    print "\033[1;32m[+]Downloading Masscan\033[1;m"
    try:
        print "\033[1;32m[+]Updating LibPcap\033[1;m"
        #proc = subprocess.Popen(config.installLibPcap, stdout=subprocess.PIPE, shell=True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to install LibPcap\033[1;m" + str(e)
    try:
        print "\033[1;32m[+]Cloning Masscan\033[1;m"
        proc = subprocess.Popen(config.cloneMasscan, stdout=subprocess.PIPE, shell=True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to clone Masscan\033[1;m" + str(e)
    #Now, compile MassDNS
    print "\033[1;32m[+]Make Masscan\033[1;m"
    try:
        proc = subprocess.Popen(config.compileMasscan, stdout=subprocess.PIPE, shell=True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to Make Masscan\033[1;m" + str(e)

def downloadEyeWitness():
    print "\033[1;32m[+]Downloading EyeWitness\033[1;m"
    try:
        print "\033[1;32m[+]Cloning EyeWitness\033[1;m"
        proc = subprocess.Popen(config.downloadEyeWitness, stdout=subprocess.PIPE, shell=True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to clone Masscan\033[1;m" + str(e)
    # Now, run Setup Script inside EyeWitness
    print "\033[1;32m[+]Setting up EyeWitness\033[1;m"
    try:
        proc = subprocess.Popen(config.setupEyeWitness, stdout=subprocess.PIPE, shell=True).wait()
    except Exception as e:
        print "\033[1;31m[-]Exception: Unable to Setup EyeWitness\033[1;m" + str(e)

def performEyeWitness(target):
    print "\033[1;32m[+]Initiating EyeWitness\033[1;m"
    cmd = './EyeWitness/EyeWitness.py --headless  -f ' + target + '.subfinder -d ' + target +".EyeWitness"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
    print "\033[1;32m[+]EyeWitness Process Completed\033[1;m"


#FINAL step, Deleting all the files created in the current directory after Making a Final Report
def deleteTempReports():
    print "\033[1;31m[-]Deleting Temporary Reports\033[1;m"
    cmd = 'rm -rf ' + target + "*"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print "\033[1;31m[-]TEMPORARY REPORTS DELETED\033[1;m"

def copyAllReports():
    print "\033[1;31m[-]Arranging Reports\033[1;m"
    cmd = 'mkdir ' + 'reports.' + target + "; cp -r " + target + ".* " + " reports." + target +"/"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print "\033[1;31m[-]TEMPORARY REPORTS DELETED\033[1;m"
















#1. Check if Go is installed, if not install Go
proc = subprocess.Popen(config.checkGoVersion, stdout=subprocess.PIPE, shell=True)
output = proc.stdout.read()
isGoInstalled = False
if output == "":
    isGoInstalled = False
    print "\033[1;32m[+]Installing Go language\033[1;m"
    #Call function to install go
    try:
        installGo()
        setGoPath()
        removeGoPackages()
        isGoInstalled = True
    except Exception as e:
        print e
else:
    print "\033[1;32m[+]Found Go language\033[1;m"
    setGoPath()
    isGoInstalled = True


#2. Check if subfinder is installed, else install it
proc = subprocess.Popen('echo $USER', stdout=subprocess.PIPE, shell=True)
if "root" in proc.stdout.read():
	proc = subprocess.Popen(config.checkSubfinderIsPresentAsRoot, stdout=subprocess.PIPE, shell = True)
	output = proc.stdout.read()
else:
	proc = subprocess.Popen(config.checkSubfinderIsPresent, stdout=subprocess.PIPE, shell = True)
	output = proc.stdout.read()
subfinderInstalled = False
if output == "":
    print "\033[1;32m[+]Installing Subfinder\033[1;m"
    #Call function to install subfinder
    installSubfinder()
    #Call Function to set PATH for Go build directory
    setGoBuildPath()
else:
    print "\033[1;32m[+]Found Subfinder\033[1;m"
    #Call Function to set PATH for Go build directory
    setGoBuildPath()

#TODO later set from OptParse
target = sys.argv[1]

#perform subfinder enumeration on the given domain
subfinderScan(target)


#DNS Resolution of IDENTIFIED subdomains
#check if massdns is installed, if not install it
if not "massdns" in os.listdir('.'):
    print "\033[1;32m[+]Installing MassDNS\033[1;m"
    #Call function to install massdns
    downloadMassDns()
else:
    print "\033[1;32m[+]Found MassDNS\033[1;m"

performMasscan(target)
filterMasscanresults(target)
createIPListFromMassDnsFilteredList(target)

#Port Scan the IP List using Masscan
#Check if Masscan is installed, if not install it

if not "masscan" in os.listdir('.'):
    print "\033[1;32m[+]Installing Masscan\033[1;m"
    #Call function to install massdns
    downloadMasscan()
else:
    print "\033[1;32m[+]Found Masscan\033[1;m"

#Perform Masscan on IP lists
#TODO MAKE IT MULTI THREADING
print "\033[1;32m[+]Initiating Masscan\033[1;m"
cmd = 'sudo ./masscan/bin/masscan -p1-65535 -iL ' + target + ".ipList "  + ' --max-rate 10000 -oG ' + target + ".masscan"
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).wait()
print "\033[1;32m[+]Masscan Completed\033[1;m"

#Perform Eyewitness on Domain lists
#Check if Eyewitness is installed, if not install it
if not "EyeWitness" in os.listdir('.'):
    print "\033[1;32m[+]Installing EyeWitness\033[1;m"
    #Call function to install massdns
    downloadEyeWitness()
else:
    print "\033[1;32m[+]Found EyeWitness\033[1;m"

performEyeWitness(target)





#FINAL STEP DELETE TEMPORARY Reports
#TODO UNCOMMENT
#copyAllReports()
#deleteTempReports()
