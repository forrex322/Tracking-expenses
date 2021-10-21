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

# All accounts
users = {
    "root": {
        "password": "gucci-mane",
        "group": "admin",
        "mail": []
    }
}


# Form validation
def validate(form):
    if len(form) > 0:
        return False
    return True


# Login authorization
def loginauth(username, password):

    conn = db.connect("main.db")
    cur = conn.cursor()
    if users:
        sql = '''
            select * from users 
            '''
    cur.execute(sql)
    results = cur.fetchall()
    return results

    if username in users:
        if password == users[username]["password"]:
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
    while True:
        username = input("New username: ")
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
    conn = db.connect("main.db")
    cur = conn.cursor()
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
        elif option == "view mail":
            print("Current mail:")
            for mail in users[username]["mail"]:
                print(mail)
        # elif users[username]["group"] == "admin":
        #     if option == "user mail":
        #         print("Whos mail would you like to see?")
        #         userinfo = input("> ")
        #         if userinfo in users:
        #             for mail in users[userinfo]["mail"]:
        #                 print(mail)
        #         else:
        #             print("There is no account with that username")
        #     elif option == "delete mail":
        #         print("Whos mail would you like to delete?")
        #         userinfo = input("> ")
        #         if userinfo in users:
        #             print("Deleting " + userinfo + "'s mail...")
        #             users[userinfo]["mail"] = []
        #             time.sleep(1)
        #             print(userinfo + "'s mail has been deleted")
        #         else:
        #             print("There is no account with that username")
        #     elif option == "delete account":
        #         print("Whos account would you like to delete?")
        #         userinfo = input("> ")
        #         if userinfo in users:
        #             print("Are you sure you want to delete " + userinfo + "'s account?")
        #             print("Options: yes | no")
        #             while True:
        #                 confirm = input("> ")
        #                 if confirm == "yes":
        #                     print("Deleting " + userinfo + "'s account...")
        #                     del users[userinfo]
        #                     time.sleep(1)
        #                     print(userinfo + "'s account has been deleted")
        #                     break
        #                 elif confirm == "no":
        #                     print("Canceling account deletion...")
        #                     time.sleep(1)
        #                     print("Account deletion canceled")
        #                     break
        #                 else:
        #                     print(confirm + " is not an option")
        #         else:
        #             print("There is no account with that username")
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
