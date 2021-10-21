# Import modules
import time
import sqlite3 as db

def init():
    conn = db.connect("main.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists users (
        username string,
        password string
        )   
    '''
    cur.execute(sql)
    conn.commit()

def test_view():
    conn = db.connect("main.db")
    cur = conn.cursor()
    sql = '''
        SELECT * FROM users
    '''
    cur.execute(sql)
    results = cur.fetchall()
    return results


# Form validation
def validate(form):
    if len(form) > 0:
        return False
    return True


# Login authorization
def loginauth(username, password):

    conn = db.connect("main.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? and password = ?", (username, password))
    found = cur.fetchone()
    if found:
        print("Login successful")
        return True
    return False


# Login
def login():
    while True:
        username = input("Username: ")
        if not len(username) > 0:
            print("Username can't be blank")
        else:
            break
    while True:
        password = input("Password: ")
        if not len(password) > 0:
            print("Password can't be blank")
        else:
            break

    if loginauth(username, password):
        return session(username)
    else:
        print("Invalid username or password")


# Register
def register():
    conn = db.connect("main.db")
    cur = conn.cursor()
    while True:
        username = input("New username: ")
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        found = cur.fetchone()
        if found:
            print("User with name is already in use, please try again")
            continue
        if not len(username) > 0:
            print("Username can't be blank")
            continue
        else:
            break
    while True:
        password = input("New password: ")
        if not len(password) > 0:
            print("Password can't be blank")
            continue
        else:
            break
    print("Creating account...")

    data = (username, password)
    sql = 'INSERT INTO users VALUES (?, ?)'
    cur.execute(sql, data)
    conn.commit()

    time.sleep(1)
    print("Account has been created")


# User session
def session(username):
    print("Welcome to your account " + username)
    print("Options: view mail | send mail | logout")
    while True:
        option = input(username + " > ")
        if option == "logout":
            print("Logging out...")
            break
        else:
            print(option + " is not an option")

# init()

print(test_view())
# On start
print("Welcome to the system. Please register or login.")
print("Options: register | login | exit")
while True:
    option = input("> ")
    if option == "login":
        login()
    elif option == "register":
        register()
    elif option == "exit":
        break
    else:
        print(option + " is not an option")


# On exit
print("Shutting down...")
time.sleep(1)
