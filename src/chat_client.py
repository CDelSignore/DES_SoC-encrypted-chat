

import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
from RSA import generate_keypair,encrypt,decrypt

#SERVER_IP    = gethostbyname( 'DE1_SoC' )
SERVER_IP = gethostbyname( '10.0.0.120' )
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )
message='hello'

#first generate the keypair
#get these two numbers from the excel file
p=1297229
q=1297619

public, private = generate_keypair(p, q)

message=('public_key: %d %d' % (public[0], public[1]))
mySocket.sendto(message.encode(),(SERVER_IP,PORT_NUMBER))
while True:
	message=input()
	message.join('\n')
        
	message_encoded = [str(encrypt(private, chars)) for chars in message]

	[mySocket.sendto(code.encode(),(SERVER_IP,PORT_NUMBER)) for code in message_encoded] # do not change [sends message through socket]
sys.exit()