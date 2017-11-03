# first of all import the socket library
import socket               
import os
import sys

fp = open("users.txt","r")
len=0
fl = fp.readlines()
# print fl
usr=[]
password=[]
len=0
for x in fl:
	a,b = x.split(" ")
	usr.append(a)
	password.append(b)
	len = len+1
	# print a

# next create a socket object
s = socket.socket()         
print "Socket successfully created"
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345               
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests 
# coming from other computers on the network
s.bind(('', port))        
print "socket binded to %s" %(port)
 
# put the socket into listening mode
s.listen(5)     
print "socket is listening"           
 
# a forever loop until we interrupt it or 
# an error occurs
while True:
 
   # Establish connection with client.
   c, addr = s.accept()     
   print 'Got connection from', addr
 
   # send a thank you message to the client. 
   c.send('Thank you for connecting')
 
   # Close the connection with the client
   c.close()