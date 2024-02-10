import ftplib
import re

host = ''
usr = ''
pwd = ''

class LauncherUpdater():
    ROOT_DIR = '/httpdocs/launcher/'
    VERSION_FILE = '.version'

    def __init__(self,versions,host,login,password):
        self.host = host
        self.login = login
        self.password = password
        self.versions = versions
        self.server = ftplib.FTP(host=host,user=login,passwd=password)

    def checkForUpdate(self,directory):
        path = self.ROOT_DIR + directory
        print('Checking updates for ' + path)
        try:
            self.server.cwd(dirname=path)
            directoryVersion = []
            self.server.retrlines(cmd='RETR ' + self.VERSION_FILE, callback=directoryVersion.append)
            print(directoryVersion)
        except ftplib.error_perm:
            print('=> ERROR => directory ' + path + ' : Pas de fichier .version ou dossier inexistant')
            return False
        if self.versions[directory] != directoryVersion[0]:
            print('Update required.', 'Current : ' + self.versions[directory], 'Available : ' + directoryVersion[0])
            return True
        return False

    def downloadDirectory(self,directory):
        path = self.ROOT_DIR + directory
        print('Download start for ' + path)
        try:
            self.server.cwd(dirname=directory)
            print(self.server.pwd())
        except ftplib.error_perm:
            pass
        
# TESTING BELOW
dl = LauncherUpdater(versions={
    'mods':'0.0.0',
    'config':'0.0.0'
}, host=host, login=usr, password=pwd)
dl.checkForUpdate('mods')