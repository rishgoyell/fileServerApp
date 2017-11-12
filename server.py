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
   # while option not in ['1','2']:

   #    try:
   #       option = clientsocket.myreceive()
   #    except Exception as e:
   #       raise e
   return option


def sign_in(clientsocket):
   curruser = user.user(clientsocket)
   try:
      clientsocket.mysend('Enter Username:Password\n')
   except Exception as e:
      raise e
   try:
      creds = clientsocket.myreceive()
   except Exception as e:
      raise e

   if creds.count(':') != 1:
      clientsocket.mysend('Information not provided in appropriate form\n')
      return False

   l = creds.strip('\n').split(':')
   curruser.update_cred(l[0],l[1])
   login_message = curruser.login()
   clientsocket.mysend(login_message)
   if 'Successful' in login_message:
      return curruser
   else:
      return False


def sign_up(clientsocket):
   try:
      clientsocket.mysend('Enter Username:Password:Password\n')
   except Exception as e:
      raise e
   try:
      creds = clientsocket.myreceive()
   except Exception as e:
      raise e
   if creds.count(':') != 2:
      clientsocket.mysend('Information not provided in appropriate form\n')
      return False

   l = creds.strip('\n').split(':')
   sign = auth.signup(l[0], l[1], l[2])
   try:
      clientsocket.mysend(sign)
   except Exception as e:
      raise e
   if 'Successful' in sign:
      return True
   else:
      return False

def get_next_action(curruser):
   try:
      clientsocket.mysend('Enter Desired Option or [0] for HELP\n')
   except Exception as e:
      raise e
   try:
      option = clientsocket.myreceive()
   except Exception as e:
      raise e
   if option == '0':
      try:
         clientsocket.mysend('Enter \n[0] HELP \n[1] List Files\n[2] Upload File\n[3] Download File \n[4] Delete File\n[5] Give Access\n[6] Revoke Access\n[7] Shared Files\n[8] Exit\n')
      except Exception as e:
         raise e
      return True
   if option == '1':
      try:
         clientsocket.mysend(curruser.ls()+'\nShared Files: \n'+curruser.shared_to_me())
      except Exception as e:
         raise e
      return True

   if option == '2':
      try:
         clientsocket.mysend("Enter File Name\n")
      except Exception as e:
         raise e
      try:
         filename = clientsocket.myreceive()
      except Exception as e:
         raise e
      if filename =='#####----#####':
         return True
      try:
         clientsocket.mysend("Transferring File............\n")
      except Exception as e:
         raise e
      try:
         filedata = clientsocket.myreceive()
      except Exception as e:
         raise e
      curruser.writefile(filename, filedata)
      return True

   if option == '3':
      try:
         clientsocket.mysend("Enter File Name\n")
      except Exception as e:
         raise e
      try:
         filename = clientsocket.myreceive()
      except Exception as e:
         raise e
      filedata = curruser.readfile(filename)
      if "File doesn't exist!!\n" == filedata:
         filedata = curruser.shared_read(filename)
         if "File is not shared with you!!\n" == filedata:
            try:
                clientsocket.mysend("File doesn't exist!!\n")
            except Exception as e:
                raise e
         else:
            try:
               clientsocket.mysend(filedata)
            except Exception as e:
               raise e
      return True

   if option == '4':
      try:
         clientsocket.mysend("Enter File Name\n")
      except Exception as e:
         raise e
      try:
         filename = clientsocket.myreceive()
      except Exception as e:
         raise e
      delete_msg = curruser.deletefile(filename)
      try:
         clientsocket.mysend(delete_msg)
      except Exception as e:
         raise e
      return True
   if option == '5':
      try:
         clientsocket.mysend("Enter Filename:Username\n")
      except Exception as e:
         raise e
      try:
         l = clientsocket.myreceive().strip('\n').split(':')
      except Exception as e:
         raise e
      msg = curruser.shareit(l[0],l[1])
      try:
         clientsocket.mysend(msg)
      except Exception as e:
         raise e
   if option == '6':
      try:
         clientsocket.mysend("Enter Filename:Username\n")
      except Exception as e:
         raise e
      try:
         l = clientsocket.myreceive().strip('\n').split(':')
      except Exception as e:
         raise e
      msg = curruser.takeback(l[0],l[1])
      try:
         clientsocket.mysend(msg)
      except Exception as e:
         raise e

   if option == '7':
      try:
         clientsocket.mysend(curruser.i_shared())
      except Exception as e:
         raise e

   if option == '8':
      try:
         clientsocket.mysend("Closing Connection...\n")
      except Exception as e:
         raise e

      return False
   return True

class mysocket(object):

   def __init__(self, sock=None):
      if sock is None:
         self.sock = socket.socket(
          socket.AF_INET, socket.SOCK_STREAM)
         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      else:
         self.sock = sock


   def bind(self, port):
      self.sock.bind((sys.argv[1], port))


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
            raise RuntimeError("socket connection broken\n")
         totalsent = totalsent + sent

   def myreceive(self):
      MSGLEN = int(self.sock.recv(10))
      chunks = []
      bytes_recd = 0
      while bytes_recd < MSGLEN:
         chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
         if chunk == '':
            raise RuntimeError("socket connection broken\n")
         chunks.append(chunk)
         bytes_recd = bytes_recd + len(chunk)
      return ''.join(chunks)

if len(sys.argv) != 2:
    print "Insufficient arguments"
serversocket = mysocket()
print "Socket successfully created"

port = 12345

serversocket.bind(port)
print "socket bound to %s" %(port)

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
      # while True:
      while True:
         option = get_option(clientsocket)

         if option == '1':
            sign_up(clientsocket)

         if option == '2':
            curruser = sign_in(clientsocket)
            if curruser:
               break
            else:
               continue

      while get_next_action(curruser):
         continue

      del(curruser)

      clientsocket.close()
      break
   else:
      clientsocket.close()
