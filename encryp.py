from cryptography.fernet import Fernet
import sqlite3

'''Creates a masterkeys table if not present already.
    Returns true if the table was present and false if the table wasn't present'''
def createMasterKeyTable():

    conn1 = sqlite3.connect('master_key.db')
    c1 = conn1.cursor()
    c1.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='masterkeys'")
    noTable = c1.fetchall()
    conn1.close()

    if str(noTable[0][0])=="0":      # Checkfing if there is any table named 'masterkeys'
        conn = sqlite3.connect('master_key.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE masterkeys (
                username TEXT,
                masterkey BLOB, 
                password TEXT)""")
        conn.commit()
        conn.close()

        return False                  # Makes login verifying faster for the first time and
    else:                             # and also saves from error if there is no any
        return True                   # table named masterkeys


def username_creator(username, password):
    ''' creates username, respective masterkey and a new table with the name of user '''
    createMasterKeyTable()
    conn1 = sqlite3.connect('master_key.db')
    c1 = conn1.cursor()
    c1.execute("SELECT masterkey FROM masterkeys WHERE username='" + username + "'")
    datas = c1.fetchall()
    conn1.commit()

    ''' Only create passwords table and new username, masterkey row if the username is unique'''
    if len(datas) == 0:
        conn2 = sqlite3.connect('encrypted_passwords.db')
        c2 = conn2.cursor()
        c2.execute("""CREATE TABLE passwords_""" + username + """ (
        name TEXT,
        encrypted_password BLOB)""")
        conn2.commit()
        conn2.close()

        master_key = Fernet.generate_key()

        ''' Username is the account username
            master_key is the key used to encrypt and decrypt the passwords
            password is the login/ account password ( this may be the master password in other password managers)
        '''

        c1.execute("INSERT INTO masterkeys VALUES (?, ?, ?)", (username, master_key, password))
        conn1.commit()
        conn1.close()
        return True                 # This signifies the username isn't taken.
    else:
        conn1.close()
        return False                # This signifies the username is already taken.


'''For veryfying login using username and master password
    will return false immediately if masterkeys table doesn't exist '''
def login_verifier(username, password):
    if not createMasterKeyTable():
        return False
    else:
        conn1 = sqlite3.connect('master_key.db')
        c1 = conn1.cursor()
        c1.execute("SELECT password FROM masterkeys WHERE username='" + username + "'")
        datas = c1.fetchall()
        conn1.commit()
        conn1.close()
        for data in datas:
            if str(data[0]) == str(password):
                return True
        return False


def encrypter(username, name, password):
    ''' returns encrypted password '''
    conn1 = sqlite3.connect('master_key.db')  # opens a connection with database containing username and master passwords
    c1 = conn1.cursor()
    c1.execute("SELECT masterkey FROM masterkeys WHERE username='" + username + "'")
    data = c1.fetchone()
    key = data[0]
    conn1.commit()
    conn1.close()                            # closes the connection

    f = Fernet(key)
    encrypted = Fernet.encrypt(f, password.encode())
    return encrypted                        # returns the encrypted password


def decrypter(username, name, row_no):
    ''' returns the decrypted password '''

    #For extracting masterkey for decryption
    conn1 = sqlite3.connect('master_key.db')         # with database containing username and masterpassword
    c1 = conn1.cursor()
    c1.execute("SELECT masterkey FROM masterkeys WHERE username ='" + username + "'")
    data = c1.fetchone()
    key = data[0]                                     # this is the salt used for decryption
    conn1.commit()
    conn1.close()

    conn2 = sqlite3.connect('encrypted_passwords.db')          # with database containing encrypted passwords
    c2 = conn2.cursor()
    c2.execute("SELECT rowid, encrypted_password FROM passwords_" + username + " WHERE name='" + name + "' and rowid=?", (row_no, ))
    f2 = c2.fetchall()

    decrypted_password = []
    for f in f2:
        decrypted_password.append(Fernet.decrypt(Fernet(key), f[1]))
    return decrypted_password



def username_retuner(username):
    '''takes the username and returns the usernames saved in the user's table in the database'''
    conn1 = sqlite3.connect('encrypted_passwords.db')
    c1 = conn1.cursor()
    c1.execute("SELECT rowid, name FROM passwords_" + username)
    datas = c1.fetchall()
    conn1.commit()
    conn1.close()
    usernames = []
    for data in datas:
        usernames.append(data)
    return usernames


def table_deleter(username):
    conn1 = sqlite3.connect('encrypted_passwords.db')
    c1 = conn1.cursor()
    c1.execute("DROP TABLE passwords_" + username)
    conn1.commit()

    ''' Creating an empty table because username isn't deleted 
    and will cause problem if user tries to save password again.'''
   
    c1.execute("""CREATE TABLE passwords_""" + username + """ (
        name TEXT,
        encrypted_password BLOB)""")
    conn1.commit()
    conn1.close()