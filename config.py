goDownloadCommand = 'wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz'
unzipGoPackage = 'tar -xvf go1.10.3.linux-amd64.tar.gz'
moveGoPackageToSystem = 'sudo cp -R go /usr/local/'
checkGoVersion = '/usr/local/go/bin/go version'
removeGoPackage = 'rm -rf go; rm -rf go1.10.3.linux-amd64.tar.gz'
setGoPath = 'export PATH="$PATH:/usr/local/go/bin/"'
setGoBuildPath = 'export PATH="$PATH:/home/$USER/go/bin/"'
checkSubfinderIsPresent = '/home/$USER/go/bin/subfinder'
subfinderDownloadAndBuildCommand = '/usr/local/go/bin/go get github.com/subfinder/subfinder'
getUserName = 'echo $USER'
downloadMassDns = 'git clone https://github.com/blechschmidt/massdns.git'
compileMassDns = 'cd massdns/;make;cd ..;'
installLibPcap = 'sudo apt-get install git gcc make libpcap-dev'
cloneMasscan = 'git clone https://github.com/robertdavidgraham/masscan'
compileMasscan = 'cd masscan; make; cd ..;'


"""
Subfinder will work after using the installation instructions however to configure Subfinder to work with certain services, you will need to have setup API keys. These following services do not work without an API key:

                            Virustotal
                            Passivetotal
                            SecurityTrails
                            Censys
                            Riddler
                            Shodan

"""
#API keys #TODO
viruTotalAPIKey = '8653a75f7dbc5ad820dc64cea2c1cc56108bfcf5814de756ff2ae4483b2b7d7c'
