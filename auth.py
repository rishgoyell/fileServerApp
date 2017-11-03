import hashlib
import os

def signup(user, passwd, pass_repeat):
    if passwd != pass_repeat:
        return "Password doesn't match!\n"
    elif ' ' in user or ' ' in passwd:
        return "Username/Password contain spaces\n"
    else:
        f = open('cred.txt', 'a+')
        entry = f.readline()
        while entry != "":
            creds = entry.split(' ')
            if creds[0] == user:
                return "Username exists!!\n"
            entry = f.readline()

        f.write(user + " " + hashlib.md5(passwd).hexdigest() + "\n")
        f.close()
        os.makedirs(user)
        f = open(user + '/.shared', 'w+')
        f.close()
        f = open(user + '/.shared_with_me', 'w+')
        f.close()
        return "Registration Successful!!\n"


def login(user, passwd):
    pwd = hashlib.md5(passwd).hexdigest()
    f = open('cred.txt', 'a+')
    entry = f.readline().strip('\n')
    while entry != "":
        creds = entry.split(' ')
        if creds[0] == user and creds[1] == pwd:
            return "Login Successful\n"
        entry = f.readline()

    f.close()
    return "Invalid Credentials!!"


def signupTest():
    a = raw_input("User: ")
    b = raw_input("Pass: ")
    c = raw_input("Pass again: ")
    print signup(a,b,c)

def loginTest():
    a = raw_input("User: ")
    b = raw_input("Pass: ")
    print login(a,b)

