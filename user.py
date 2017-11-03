import auth
import os
from server import mysocket

class user:

    def __init__(self, name=None, passwd=None, sock):
        self.name = name
        self.pwd = passwd
        self.path = ""
        self.logged_in = False
        self.sock = sock

    def update_cred(self, name, passwd):
        self.name = name
        self.pwd = passwd

    def login(self):
        if "Invalid" in auth.login(self.name, self.pwd):
            del self
            self.sock.mysend("Invalid Credentials!!\n")
        else:
            logged_in = True
            path = self.name + '/'
            self.sock.mysend("Login Successful!!\n")

    def ls(self):
        files = os.listdir(self.path)
        flist = "\n".join(files)
        self.sock.mysend(flist)

    def readfile(self, filename):
        if os.path.isfile(self.path + filename):
            f = open(self.path + filename, "r")
            self.sock.mysend(f.read())
            f.close()
        else:
            self.sock.mysend("File doesn't exist!!\n")

    def writefile(self, filename, data):
        if os.path.isfile(self.path + filename):
            self.sock.mysend("File already exists, do you want to overwrite?")
            overwrite = self.sock.myrecieve()
            overwrite = overwrite.strip('\n')
            if overwrite == "yes" or overwrite == "y" or overwrite == "Y" or overwrite == "Yes":
                f = open(self.path + filename, "w")
                f.write(data)
                f.close()
                self.sock.mysend("File written successfully!!\n")
            else:
                self.sock.mysend("Didn't overwrite file\n")
        else:
            f = open(self.path + filename, "w")
            f.write(data)
            f.close()
            self.sock.mysend("File written successfully!!\n")



