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
            return "Invalid Credentials!!\n"
        else:
            logged_in = True
            self.path = self.name + '/'
            return "Login Successful!!\n"

    def ls(self):
        files = filter( lambda f: not f.startswith('.'), os.listdir(self.path))
        flist = "\n".join(files)
        return flist

    def i_shared(self):
        f = open(self.path + ".shared", "r")
        slist = f.read()
        f.close()
        return slist

    def shared_to_me(self):
        f = open(self.path + ".shared_with_me", "r")
        slist = f.read()
        f.close()
        return slist

    def shareit(self, filename, who):
        if os.path.isfile(self.path + filename):
            f = open('cred.txt', 'r')
            entry = f.readline()
            found = False
            while entry != "":
                creds = entry.split(' ')
                if creds[0] == who:
                    found = True
                    break
                entry = f.readline()
            f.close()
            if not found :
                return "User doesn't exist!!\n"
            f = open(self.path + ".shared", "a+")
            f.write(filename + " " + who + "\n")
            f.close()
            f = open(self.path + "../" + who + "/.shared_with_me", "a+")
            f.write(filename + " " + self.name + "\n")
            f.close()
            return "File shared!!\n"
        else:
            return "File doesn't exist!!\n"

    def takeback(self, filename, who):
        f = open('cred.txt', 'r')
        entry = f.readline()
        found = False
        while entry != "":
            creds = entry.split(' ')
            if creds[0] == who:
                found = True
                break
            entry = f.readline()
        f.close()
        if not found:
            return "User doesn't exist!!\n"
        f = open(self.path + ".shared", "w+")
        lines = f.readlines()
        for line in lines:
            if line != filename + ' ' + who + "\n":
                f.write(line)
        f.close()
        f = open(self.path + "../" + who + "/.shared_with_me", "w+")
        lines = f.readlines()
        for line in lines:
            if line != filename + ' ' + self.name + "\n":
                f.write(line)
        f.close()
        return "Access has been successfully removed!\n"

    def shared_read(self, filename):
        f = open(self.path + '.shared_with_me', 'r')
        entry = f.readline().strip('\n')
        found = False
        owner = ""
        while entry != "":
            creds = entry.split(' ')
            if creds[0] == filename:
                found = True
                owner = creds[1]
                break
            entry = f.readline().strip('\n')
        f.close()
        if not found:
            return "File is not shared with you!!\n"
        if os.path.isfile(self.path + '../' + owner + '/' + filename):
            f = open(self.path + '../' + owner + '/' + filename, "r")
            data = f.read()
            f.close()
            return data
        else:
            f = open(self.path + ".shared_with_me", "w+")
            lines = f.readlines()
            for line in lines:
                if line != filename + ' ' + owner + "\n":
                    f.write(line)
            f.close()
            return "File doesn't exist!!\n"



    def readfile(self, filename):
        if os.path.isfile(self.path + filename):
            f = open(self.path + filename, "r")
            data = f.read()
            f.close()
            return data
        else:
            return "File doesn't exist!!\n"

    def writefile(self, filename, data):
        if os.path.isfile(self.path + filename):
            i=1
            while os.path.isfile(self.path + filename + " (" + str(i) +")"):
                i+=1
            filename += " (" + str(i) +")"
        f = open(self.path + filename, "w+")
        f.write(data)
        f.close()
        return "File written successfully!!\n"

    def deletefile(self, filename):
        if os.path.isfile(self.path + filename):
            os.remove(self.path + filename)
            f = open(self.path + ".shared", "w+")
            lines = f.readlines()
            for line in lines:
                if line.split(' ')[0] != filename:
                    f.write(line)
            f.close()
            return "File removed successfully!!\n"
        else:
            return "File doesn't exist!!\n"

    def __exit__(self, *err):
        self.close()

