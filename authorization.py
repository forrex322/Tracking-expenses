from main import init_db, insert_expenses, delete_info, db, view, view_by_time, view_by_year, view_by_month


def init_users():
    conn = db.connect("main.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username string,
        password string
        )   
    '''
    cur.execute(sql)
    conn.commit()


# Form validation
def validate(form):
    if len(form) > 0:
        return False
    return True


# Login authorization
def login_auth(username, password):
    conn = db.connect("main.db")
    cur = conn.cursor()
    cur.execute("select * from users where username = ? and password = ?", (username, password))
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

    if login_auth(username, password):
        return session(username)
    else:
        print("Invalid username or password")


# Register
def register():
    conn = db.connect("main.db")
    cur = conn.cursor()
    while True:
        username = input("New username: ")
        cur.execute("select * from users where username = ?", (username,))
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
    sql = 'insert into users (username, password) values (?, ?)'
    cur.execute(sql, data)
    conn.commit()

    print("Account has been created")


# User session
def session(username):
    print("Welcome to your account " + username)
    print("Options: expenses | logout")
    while True:
        option = input(username + " > ")
        if option == "expenses":
            main(username)
            continue
        if option == "logout":
            print("Logging out...")
            break
        else:
            print(option + " is not an option")


def main(username):
    init_db()
    while True:
        choice = input(
            "Enter the number \n1. Insert info \n2. Show all info \n3. Show certain info \n4. Delete all info \n5. Show info by certain time \n6. Exit\n")
        if choice == "1":
            amount = input("Enter the amount\n")
            category = input("Enter the category\n")
            message = input("Enter the information\n")
            date = input("Enter the date(YYYY-MM-DD) or leave this field blank, then the current date will be set\n")
            insert_expenses(username, amount, category, message, date)

        elif choice == "2":
            print(view(username, category=None))

        elif choice == "3":
            category = input("Enter the category to show info\n")
            print(view(username, category))

        elif choice == "4":
            delete_info(username)

        elif choice == "5":
            time_choice = input("Enter the number \n1. Show by day \n2. Show by month \n3. Show by year\n")
            if time_choice == "1":
                date = input("Enter the date(YYYY-MM-DD)\n")
                print(view_by_time(username, date))

            elif time_choice == "2":
                date = input("Enter the month(YYYY-MM)\n")
                print(view_by_month(username, date))

            elif time_choice == "3":
                date = input("Enter the year(YYYY)\n")
                print(view_by_year(username, date))

            else:
                print("Please choose correct number")

        elif choice == "6":
            break

        else:
            print("Please choose correct number")


def start():
    init_users()
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
            # On exit
            print("Shutting down...")
            break
        else:
            print(option + " is not an option")
