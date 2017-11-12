import socket
import getpass         
import os
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
ip_address = raw_input("Please type the ip address to connect to, and then press enter\n")
s.connect(ip_address,port)
while True:
	option = 0
	option_msg = s.myreceive()
	while option not in ['1','2']:
		option = raw_input(option_msg)
		if option not in ['1','2']:
			print "Error: Enter 1 or 2"
	s.mysend(option)
	if option == '1':
		s.myreceive()
		username = raw_input("Username:")
		password = getpass.getpass("Password:")
		password_repeat = getpass.getpass("Re-enter Password:")
		s.mysend(username+':'+password+':'+password_repeat)
	if option == '2':
		s.myreceive()
		username = raw_input("Username:")
		password = getpass.getpass("Password:")
		s.mysend(username+':'+password)
	login_msg = s.myreceive()
	print login_msg
	if 'Successful' in login_msg and option == '2':
		break

while True:
	option = -1
	option_msg = s.myreceive()
	while option not in ['0','1','2', '3', '4', '5','6','7','8']:
		option = raw_input(option_msg)
		if option not in ['0','1','2', '3', '4', '5','6','7','8']:
			print "Error: Enter valid option"
	s.mysend(option)
	try:
		msg = s.myreceive()
		print msg
	except Exception as e:
		raise e

	if option == '2':
		filename = raw_input()
		if os.path.isfile(filename):
			f = open(filename, "r")
			filedata = f.read()
			f.close()
			s.mysend(os.path.basename(filename))
			print s.myreceive()
			s.mysend(filedata)
		else:
			s.mysend("#####----#####")
			print "File doesn't exist!!\n"
	elif option == '3':
		filename = raw_input()
		filename = os.path.basename(filename)
		s.mysend(filename)
		filedata = s.myreceive()
		if "File doesn't exist!!\n" == filedata:
			print filedata
		else:
			with open(filename, 'w') as outfile:
				outfile.write(filedata)
			print("File Transferred!!")

	elif option == '4':
		filename = raw_input()
		filename = os.path.basename(filename)
		s.mysend(filename)
		print s.myreceive()

	elif option in ['5','6']:
		try:
			l = ''
			while l.count(':') != 1:
				l=raw_input()
				if l.count(':') !=1:
					print "Follow correct syntax\n"
			s.mysend(l)
		except Exception as e:
			raise e
		try:
			print s.myreceive()
		except Exception as e:
			raise e

	elif option == '8':
		break
		s.close()

s.close()
       