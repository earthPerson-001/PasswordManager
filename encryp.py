from cryptography.fernet import Fernet
import sqlite3

conn = sqlite3.connect('encryption.db')
c = conn.cursor()
    
'''c.execute("""CREATE TABLE masterkeys (
          username TEXT,
           masterkey BLOB, 
           password TEXT)""")
conn.commit()'''


def username_creator(username, password):
    ''' creates username, respective masterkey and a new table with the name of user '''
    conn1 = sqlite3.connect('encryption.db')
    c1 = conn1.cursor()
    c1.execute("SELECT masterkey FROM masterkeys WHERE username='" + username + "'")
    datas = c1.fetchall()
    conn1.commit()
    if len(datas) == 0:
        conn2 = sqlite3.connect('encryption.db')
        c2 = conn2.cursor()
        c2.execute("""CREATE TABLE passwords_""" + username + """ (
        name TEXT,
         encrypted_password BLOB)""")
        conn2.commit()
        conn2.close()

        master_key = Fernet.generate_key()
        c1.execute("INSERT INTO masterkeys VALUES (?, ?, ?)", (username, master_key, password))
        conn1.commit()
        conn1.close()
        return True
    else:
        conn1.close()
        return False


def login_verifier(username, password):
    conn1 = sqlite3.connect('encryption.db')
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
    conn1 = sqlite3.connect('encryption.db')  # opens a connection with database
    c1 = conn1.cursor()
    c1.execute("SELECT masterkey FROM masterkeys WHERE username='" + username + "'")
    data = c1.fetchone()
    key = data[0]
    conn1.commit()
    conn1.close()                            # closes the connection
    f = Fernet(key)
    encrypted = Fernet.encrypt(f, password.encode())

    conn2 = sqlite3.connect('encryption.db')  # opens another connection
    c2 = conn2.cursor()
    c2.execute("""INSERT INTO passwords_""" + username + """ 
      VALUES
      (?, ?)""", (name, encrypted))
    conn2.commit()
    conn2.close()
    return encrypted


def decrypter(username, name, row_no):
    ''' returns the decrypted password '''
    conn1 = sqlite3.connect('encryption.db')
    c1 = conn1.cursor()
    c1.execute("SELECT masterkey FROM masterkeys WHERE username ='" + username + "'")
    data = c1.fetchone()
    key = data[0]
    conn1.commit()
    conn1.close()

    conn2 = sqlite3.connect('encryption.db')
    c2 = conn2.cursor()
    c2.execute("SELECT rowid, encrypted_password FROM passwords_" + username + " WHERE name='" + name + "' and rowid=?", (row_no, ))
    f2 = c2.fetchall()

    decrypted_password = []
    for f in f2:
        decrypted_password.append(Fernet.decrypt(Fernet(key), f[1]))
    return decrypted_password



def username_retuner(username):
    '''takes the username and returns the usernames saved in the user's table in the database'''
    conn1 = sqlite3.connect('encryption.db')
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
    conn1 = sqlite3.connect('encryption.db')
    c1 = conn1.cursor()
    c1.execute("DROP TABLE passwords_" + username)
    conn1.commit()
    conn1.close()
#conn.close()
