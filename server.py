import socket               
import os
import sys
import time
import auth
import user

def get_option(clientsocket):
   try:
      clientsocket.mysend('[1] Sign Up \n[2] Sign In\n')
   except Exception as e:
      raise e
   try:
      option = clientsocket.myreceive()
   except Exception as e:
      raise e
   while option not in ['1','2']:
      try:
         clientsocket.send('Option Not Valid: Please enter \'1\' or \'2\'')
      except Exception as e:
         raise e
      try:
         option = clientsocket.myreceive()
      except Exception as e:
         raise e
   return option


def sign_in(clientsocket):
   curruser = user.user(clientsocket)
   try:
      clientsocket.mysend('Enter Username:Password')
   except Exception as e:
      raise e
   try:
      # print "accepting creds"
      creds = clientsocket.myreceive()
      # print "accepted creds"
   except Exception as e:
      raise e

   if creds.count(':') != 1:
      clientsocket.mysend('Information not provided in appropriate form')
      return False

   l = creds.strip('\n').split(':')
   curruser.update_cred(l[0],l[1])
   login_message = curruser.login()
   clientsocket.mysend(login_message)
   if 'Successful' in login_message:
      return True
   else:
      return False


      # sign = auth.signup(l[0], l[1], l[2])
      # try:
      #    clientsocket.mysend(sign)
      # except Exception as e:
      #    raise e
      # return 1


def sign_up():
   return True

   # elif option == '2':
   #    try:
   #       clientsocket.mysend('Send the credentials')
   #    except Exception as e:
   #       flag = 0
   #       print "connection broke"
   #       break;
   #    try:
   #       creds = clientsocket.myreceive()
   #    except Exception as e:
   #       raise e
   #    l = creds.strip('\n').split(':')
   #    sign = auth.login(l[0], l[1])
   #    try:
   #       clientsocket.mysend(sign)
   #    except Exception as e:
   #       raise e
   #    return 2
   # else :
   #    clientsocket.mysend('option not recognized: Please send 1 or 2')
   #    return 0

class mysocket(object):

   def __init__(self, sock=None):
      if sock is None:
         self.sock = socket.socket(
          socket.AF_INET, socket.SOCK_STREAM)
      else:
         self.sock = sock


   def bind(self, port):
      self.sock.bind((socket.gethostname(), port))


   def connect(self, host, port):
      self.sock.connect((host, port))


   def listen(self, num_clients):
      self.sock.listen(num_clients)


   def accept(self):
      c, addr = self.sock.accept()
      clientSocket = mysocket(c)
      return [clientSocket,addr]

   def close(self):
      self.sock.close()

   def mysend(self, msg):
      MSGLEN = len(msg)
      length = str(MSGLEN)
      if len(length) <= 10:
         length = '0'*(10-len(length))+length
      else:
         print "increased length"
      msg= length+msg
      totalsent = 0
      while totalsent < MSGLEN+10:
         sent = self.sock.send(msg[totalsent:])
         if sent == 0:
            raise RuntimeError("socket connection broken")
         totalsent = totalsent + sent

   def myreceive(self):
      MSGLEN = int(self.sock.recv(10))
      chunks = []
      bytes_recd = 0
      while bytes_recd < MSGLEN:
         chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
         if chunk == '':
            raise RuntimeError("socket connection broken")
         chunks.append(chunk)
         bytes_recd = bytes_recd + len(chunk)
      return ''.join(chunks)


serversocket = mysocket()       
print "Socket successfully created"

port = 12345               

serversocket.bind(port)     
print "socket binded to %s" %(port)
 
serversocket.listen(5)     
print "socket is listening"           
 
while True:
 
   clientsocket, addr = serversocket.accept()     
   print 'Got connection from', addr
   newpid = os.fork()
   if newpid<0 :
      print "error in forking"
      sys.exit()
   elif newpid==0 :
      flag = 1
      while True:

         while True:
            option = get_option(clientsocket)
            if option == '1':
               if sign_up():
                  break
               else:
                  continue
            if option == '2':
               print "send credentials!!"
               if sign_in(clientsocket):
                  break
               else:
                  continue


      if not flag :
         break
      break
   else:
      clientsocket.close()

serversocket.close()
