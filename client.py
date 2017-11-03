import socket               
 
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

s = mysocket()
port = 12345               
 
s.connect('127.0.0.1',port)
# print s.myreceive()
option = raw_input(s.myreceive())
s.mysend(option)
print s.myreceive()
if option == '1':
	creds = raw_input("username:password:password_repeat\n")
	s.mysend(creds)
elif option == '2':
	creds = raw_input("username:password\n")
	s.mysend(creds)
print s.myreceive()
	
s.close()       