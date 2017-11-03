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
            self.path = self.name + '/'
            return ("Login Successful!!\n")

    def ls(self):
        files = os.listdir(self.path)
        flist = "\n".join(files)
        return (flist)

    def what_shared(self):
        f = open(self.path + ".shared", "r")
        slist = f.read()
        f.close()
        return slist

    def readfile(self, filename):
        if os.path.isfile(self.path + filename):
            f = open(self.path + filename, "r")
            data = f.read()
            f.close()
            return (data)
        else:
            return ("File doesn't exist!!\n")

    def writefile(self, filename, data):
        if os.path.isfile(self.path + filename):
            i=1
            while os.path.isfile(self.path + filename + "\ \(" + i +"\)"):
                i+=1
            filename += "\ \(" + i +"\)"
        f = open(self.path + filename, "w")
        f.write(data)
        f.close()
        return ("File written successfully!!\n")

    def deletefile(self, filename):
        if os.path.isfile(self.path + filename):
            os.remove(self.path + filename)
            return "File removed successfully!!\n"
        else:
            return "File doesn't exist!!\n"

    def __exit__(self, *err):
        self.close()

