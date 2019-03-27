#! /usr/bin/env python

# Importacion de namespaces

import getopt
import sys
from docx import Document
from ssh2.session import Session
import socket

# Lectura del archivo de configuracion

with open('conf/main.cfg') as file:
	for line in file:
			hostname_raw = line.split(':',1)[1]
			hostname = hostname_raw.split()[0]
                        cisco_ip_raw = line.split(':',2)[1]
			cisco_ip = cisco_ip_raw.split()[0]


try:
	opts, args = getopt.getopt(sys.argv[1:], "u:p:", ['user=', 
                                                            'password=',
                                                           ])
except  getopt.error, msg:
	print(msg)
for opt, arg in opts:
	if opt in ('-u', '--user'):
        	ciscoUser = arg
    	elif opt in ('-p', '--password'):
		ciscoPass = arg
    	elif not opts:
        	print "Error: ciscoBackup {-u|--user} <user> {-p|--password} <password>"

# Funcion de ejecucion de comandos mediante ssh

def conexionSSH (dest_host, comando):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((dest_host, 22))

        session = Session()
	session.handshake(sock)
	session.userauth_password(ciscoUser, ciscoPass)

	channel = session.open_session()
	channel.execute(comando)
	size, data = channel.read()
	if size > 0 :
		comandoOut =  data.decode('utf-8')
	channel.close()

	return comandoOut


# Comandos a ejecutar para la recogida de informacion


ciscoOut = conexionSSH (hostname, 'show ver')


# Escritura de documento Word basandose en plantilla y relleneando con los datos obtenidos de la ejecucion de los comandos

print ciscoOut
