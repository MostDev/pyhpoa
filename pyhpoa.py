#HP OA Firmware Upgrader V0.1
#Thomas Attree
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import paramiko
import ConfigParser
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def sshUpgrade(target,username,password,ip,firmFile):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	try:
		ssh.connect(target,username,password)
	except:
		print ('[-] Could not connect to target' + target)
		return

	#Send update force command
	stdin, stdout, stderr = ssh.exec_command("update image force ftp://" + ip + ":2121/" + firmFile)

	#Accept warning
	stdin.write("Y\n")
	stdin.flush()
	
	data = stdout.read.splitlines()
	for line in data:
		print (line)
	return

def ftpServer(directory):
	#Define authoriser
	authorizer = DummyAuthorizer()
	#Define anonymous user
	authorizer.add_anonymous(directory)

	#Instantiate FTP handler class
	handler = FTPHandler
	handler.authorizer = authorizer

	#Setup FTP log
	logging.basicConfig(filename=os.getcwd(), level = logging.DEBUG)

	#Instantiate FTP server class and listener
	address = ('0.0.0.0', 2121)
	server = FTPServer(address, handler)

	#Max limit for connections
	server.max_cons = 256
	server.max_cons_per_ip = 5

	#Start FTP server
	try:
		server.serve_forever()
		print ('[+] FTP server started')
	except:
		print ('[-] Could not start FTP server')


def main():
	config = ConfigParser.ConfigParser()
	config.read('pyhpoa.conf')

	try:
		try:
			targets = config.get('targets','oaip').split(',')
			for target in targets:
				print ('[+] ' + target)
		except:
			print ('[-] Unable to get target addresses')

		try:
			directory = config.get('firmware','directory')
			print ('[+] Firmware directory for FTP server: ' + directory)
		except:
			print ('[-] Could not get FTP directory')

		try:
			firmFile = config.get('firmware','file')
			print ('[+] Firmware file: ' + firmFile)
		except:
			print ('[-] Could not get FTP directory')
		try:
			ip = config.get('firmware','FTPServerIP')
			print ('[+] FTP Server IP: ' + ip)
		except:
			print ('[-] Could not get FTP Server IP')

		try:
			username = config.get('credentials','user')
			print ('[+] Username ' + username + ' will be used')
		except:
			print ('[-] Could not get username')

		try:
			password = config.get('credentials','password')
			print ('[+] Password ' + password + ' will be used')
		except:
			print ('[-] Could not get Password')

	except:
		print ('[-] Config errors. Please check the configuration and run script again')
		exit(0)

	#Start FTP server
	ftpServer(directory)

	for target in targets:
		sshUpgrade(target,username,password,ip,firmFile)
		print (target)

if __name__ == '__main__':
	main()
