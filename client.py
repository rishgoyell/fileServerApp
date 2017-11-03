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
while True:
	option = 0
	option_msg = s.myreceive()
	while option not in ['1','2']:
		option = raw_input(option_msg)
		if option not in ['1','2']:
			print "Error: Enter 1 or 2"
	s.mysend(option)

	creds = raw_input(s.myreceive())
	s.mysend(creds)
	login_msg = s.myreceive()
	print login_msg
	if 'Successful' in login_msg and option == '2':
		break

while True:
	option = 0
	option_msg = s.myreceive()
	while option not in ['1','2', '3', '4', '5']:
		option = raw_input(option_msg)
		if option not in ['1','2', '3', '4', '5']:
			print "Error: Enter valid option"
	s.mysend(option)
	try:
		msg = s.myreceive()
		print msg
	except Exception as e:
		raise e
	if option == '1':
		continue

	if option == '2':
		filename = raw_input()
		if os.path.isfile(filename):
			f = open(filename, "r")
			filedata = f.read()
			f.close()
			s.mysend(os.path.basename(filename))
		else:
			print "File doesn't exist!!\n"
	if option == '3':
		filename = raw_input()
		s.mysend(filename)
		filedata = s.myreceive()
		with open(filename, 'w') as outfile:
			outfile.write(filedata)

	if option == '4':
		filename = raw_input()
		s.mysend(filename)
		print s.myreceive()

	if option == '5':
		break

		
s.close()       