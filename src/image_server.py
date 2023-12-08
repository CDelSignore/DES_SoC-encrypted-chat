from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import re
import struct
from RSA import decrypt
import des


PORT_NUMBER = 5000
SIZE = 8192

#hostName = gethostbyname( 'DE1_SoC' )
hostName = gethostbyname( '10.0.0.120' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))
client_public_key=''
des_key=''
while True:
	(data,addr) = mySocket.recvfrom(SIZE)
	data=data.decode()
	if data.find('public_key')!=-1: #client has sent their public key
		(public_key_e, public_key_n) = [int(s) for s in data[12:].split()]
		client_public_key = (public_key_e, public_key_n)
		print ('public key is : %d, %d'%(public_key_e,public_key_n))

	elif data.find('des_key')!=-1: #client has sent their DES key
		#read the next 8 bytes for the DES key by running (data,addr) = mySocket.recvfrom(SIZE) 8 times and then decrypting with RSA
		for i in range(8):
			(data,addr) = mySocket.recvfrom(SIZE)
			cipher=int(data)
			des_key += decrypt(client_public_key, cipher)

		print ('DES key is :' + des_key)
		#now we will receive the image from the client
		(data,addr) = mySocket.recvfrom(SIZE)
		#decrypt the image
            	
		decoder = des.des()
		rr = decoder.decrypt(des_key, data, cbc=False)
		rr_byte=bytearray()
		for x in rr:
			rr_byte += bytes([ord(x)])

		#write to file to make sure it is okay
		file2=open(r'penguin_decrypted.jpg',"wb") 
		file2.write(bytes(rr_byte))
		file2.close()
		print ('decypting image completed')
		break
	else:
		continue



