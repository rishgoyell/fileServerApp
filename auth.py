import hashlib

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
        return "Registration Successful!!\n"


a = raw_input("Username: ")
b = raw_input("Pass: ")
c = raw_input("Pass again: ")

print signup(a, b, c)
