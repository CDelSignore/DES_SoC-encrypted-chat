from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import re
from RSA import decrypt
PORT_NUMBER = 5000
SIZE = 1024

#hostName = gethostbyname( 'DE1_SoC' )
hostName = gethostbyname( '10.0.0.120' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))
client_public_key=''
while True:
	(data,addr) = mySocket.recvfrom(SIZE)
	data=data.decode()
	if data.find('public_key')!=-1: #client has sent their public key
		(public_key_e, public_key_n) = [int(s) for s in data[12:].split()]
		client_public_key = (public_key_e, public_key_n)
		print ('public key is : %d, %d'%(public_key_e,public_key_n))
	else:
		cipher=int(data)
		data_decoded = decrypt(client_public_key, cipher)
		print (":", data_decoded)

sys.ext()
#What could I be doing wrong?

