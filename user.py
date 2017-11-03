import auth
import os

class user:

    def __init__(self,sock, name=None, passwd=None):
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
            return ("Invalid Credentials!!\n")
        else:
            logged_in = True
            path = self.name + '/'
            return ("Login Successful!!\n")

    def ls(self):
        files = os.listdir(self.path)
        flist = "\n".join(files)
        return (flist)

    def readfile(self, filename):
        if os.path.isfile(self.path + filename):
            f = open(self.path + filename, "r")
            return (f.read())
            f.close()
        else:
            return ("File doesn't exist!!\n")

    def writefile(self, filename, data):
        if os.path.isfile(self.path + filename):
            return ("File already exists, do you want to overwrite?")
            # overwrite = self.sock.myrecieve()
            overwrite = overwrite.strip('\n')
            if overwrite == "yes" or overwrite == "y" or overwrite == "Y" or overwrite == "Yes":
                f = open(self.path + filename, "w")
                f.write(data)
                f.close()
                return ("File written successfully!!\n")
            else:
                return ("Didn't overwrite file\n")
        else:
            f = open(self.path + filename, "w")
            f.write(data)
            f.close()
            return ("File written successfully!!\n")



