from functional import (
    init_db, insert_expenses, delete_user_expenses, view, view_by_day, view_by_year, view_by_month, db
)
from settings import (
    DATABASE_NAME, MENU_ITEMS, EXIT_COMMAND, INSERT_COMMAND,
    VIEW_USER_EXPENSES_COMMAND, VIEW_BY_TIME_EXPENSES_COMMAND,
    VIEW_BY_CERTAIN_CATEGORY_COMMAND, DELETE_USER_EXPENSES_COMMAND,
    VIEW_BY_DATE_COMMAND, VIEW_BY_MONTH_COMMAND,
    VIEW_BY_YEAR_COMMAND
)


def init_users():
    conn = db.connect(DATABASE_NAME)
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
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("select * from users where username = ? and password = ?", (username, password))
    found = cur.fetchone()
    if found:
        print("Login successful")
        return True
    return False


def get_username():
    return get_user_not_empty_input("Hint: username can't be blank\nUsername: ")


def get_password():
    return get_user_not_empty_input("Hint: password can't be blank\nPassword: ")


def get_user_not_empty_input(description):
    field = ""
    while len(field) == 0:
        field = input(description)
    return field


# Login
def login():
    username = get_username()
    password = get_password()

    if login_auth(username, password):
        user_menu(username)
    else:
        print("Invalid username or password")


# Register
def register():
    conn = db.connect(DATABASE_NAME)
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
def user_menu(username):
    print("Welcome to your account " + username)
    print("Options: expenses | logout")
    while True:
        option = input(username + " > ")
        if option == "logout":
            print("Logging out...")
            break
        elif option == "expenses":
            expenses_menu(username)
        else:
            print(option + " is not an option")


def expenses_menu(username):
    init_db()
    choice_menu = {
        INSERT_COMMAND: insert_expenses_choice,
        VIEW_USER_EXPENSES_COMMAND: view_user_expenses_choice,
        VIEW_BY_CERTAIN_CATEGORY_COMMAND: view_by_certain_category_choice,
        DELETE_USER_EXPENSES_COMMAND: delete_user_expenses,
        VIEW_BY_TIME_EXPENSES_COMMAND: view_by_time_choice
    }

    while True:
        choice = input(MENU_ITEMS)
        if choice in choice_menu:
            choice_menu[choice](username)

        elif choice == EXIT_COMMAND:
            break

        else:
            print("Please choose correct number")


def view_by_time_choice(username):
    choice_menu = {
        VIEW_BY_DATE_COMMAND: (view_by_day, "Enter the date(YYYY-MM-DD)\n"),
        VIEW_BY_MONTH_COMMAND: (view_by_month, "Enter the date(YYYY-MM)\n"),
        VIEW_BY_YEAR_COMMAND: (view_by_year, "Enter the date(YYYY)\n")
    }
    time_choice = input("Enter the number \n1. Show by day \n2. Show by month \n3. Show by year\n")
    if time_choice in choice_menu:
        date = input(choice_menu[time_choice][1])
        print(choice_menu[time_choice][0](username, date))

    else:
        print("Please choose correct number")


def view_by_certain_category_choice(username):
    category = input("Enter the category to show info\n")
    print(view(username, category))


def view_user_expenses_choice(username):
    print(view(username, category=None))


def insert_expenses_choice(username):
    amount = input("Enter the amount\n")
    category = input("Enter the category\n")
    message = input("Enter the information\n")
    date = input("Enter the date(YYYY-MM-DD) or leave this field blank, then the current date will be set\n")
    insert_expenses(username, amount, category, message, date)
