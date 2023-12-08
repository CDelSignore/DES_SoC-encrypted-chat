
import des
import sys
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname
from RSA import generate_keypair,encrypt,decrypt
import struct


#SERVER_IP = gethostbyname( 'DE1_SoC' )
SERVER_IP = gethostbyname( '10.0.0.120' )
PORT_NUMBER = 5000
SIZE = 1024
des_key='secret_k'
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
#send des_key
message=('des_key')
mySocket.sendto(message.encode(),(SERVER_IP,PORT_NUMBER))

des_encoded = [str(encrypt(private, chars)) for chars in des_key]

[mySocket.sendto(code.encode(),(SERVER_IP,PORT_NUMBER)) for code in des_encoded]
#read image, encode, send the encoded image binary file
file=open(r'penguin.jpg',"rb") 
data=file.read()
file.close()

coder = des.des()
r = coder.encrypt(des_key, data, cbc=False)
r_byte=bytearray()
for x in r:
	r_byte += bytes([ord(x)])

#send image through socket
mySocket.sendto(bytes(r_byte),(SERVER_IP,PORT_NUMBER))
print('encrypted image sent!')

