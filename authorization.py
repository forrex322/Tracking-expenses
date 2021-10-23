import bcrypt
from functional import (
    init_db, insert_expenses, delete_user_expenses, view, view_by_day, view_by_year, view_by_month, db
)
from settings import (
    DATABASE_NAME, MENU_ITEMS, EXIT_COMMAND, INSERT_COMMAND,
    VIEW_USER_EXPENSES_COMMAND, VIEW_BY_TIME_EXPENSES_COMMAND,
    VIEW_BY_CERTAIN_CATEGORY_COMMAND, DELETE_USER_EXPENSES_COMMAND,
    VIEW_BY_DATE_COMMAND, VIEW_BY_MONTH_COMMAND,
    VIEW_BY_YEAR_COMMAND, HINT_PASSWORD_COMMAND, HINT_USERNAME_COMMAND,
    INVALID_CREDENTIALS_COMMAND, SUCCESSFUL_LOGIN_COMMAND,
    ENTER_THE_DATE_COMMAND, NEW_USER_COMMAND, USER_ALREADY_CREATED_COMMAND,
    NOT_BLANK_USER_COMMAND, NEW_PASSWORD_COMMAND, NOT_BLANK_PASSWORD_COMMAND,
    CREATING_ACCOUNT_COMMAND, CREATED_ACCOUNT_COMMAND, CHOOSE_CORRECT_NUMBER_COMMAND,
    WELCOME_COMMAND, OPTIONS_COMMAND, LOGOUT_COMMAND, LOGGING_OUT_COMMAND, EXPENSES_COMMAND,
    NOT_OPTION_COMMAND, ENTER_THE_CATEGORY_COMMAND, ENTER_THE_TIME_CHOICE_COMMAND, ENTER_THE_AMOUNT_COMMAND,
    ENTER_THE_CATEGORY_TO_SHOW_INFO_COMMAND, ENTER_THE_INFORMATION_COMMAND, ENTER_THE_DATE_OR_LEAVE_BLANK_FIELD_COMMAND,
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


# Login authorization
def login_auth(username, password):
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute("select * from users where username = ?", (username,))
    found = cur.fetchone()
    if not found:
        return False
    found_hash_password_sql = found[2]

    if bcrypt.checkpw(password.encode("utf8"), found_hash_password_sql):
        print(SUCCESSFUL_LOGIN_COMMAND)
        return True
    return False


def get_username():
    return get_user_not_empty_input(HINT_USERNAME_COMMAND)


def get_password():
    return get_user_not_empty_input(HINT_PASSWORD_COMMAND)


def get_user_not_empty_input(description):
    field = ""
    while not field:
        field = input(description)
    return field


# Login
def login():
    username = get_username()
    password = get_password()

    if login_auth(username, password):
        user_menu(username)
    else:
        print(INVALID_CREDENTIALS_COMMAND)


# Register
def register():
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()
    while True:
        username = input(NEW_USER_COMMAND)
        cur.execute("select * from users where username = ?", (username,))
        found = cur.fetchone()
        if found:
            print(USER_ALREADY_CREATED_COMMAND)
            continue
        if not len(username) > 0:
            print(NOT_BLANK_USER_COMMAND)
            continue
        else:
            break
    while True:
        password = input(NEW_PASSWORD_COMMAND)
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        password = hashed_password
        if not len(password) > 0:
            print(NOT_BLANK_PASSWORD_COMMAND)
            continue
        else:
            break
    print(CREATING_ACCOUNT_COMMAND)

    data = (username, password)
    sql = 'insert into users (username, password) values (?, ?)'
    cur.execute(sql, data)
    conn.commit()

    print(CREATED_ACCOUNT_COMMAND)


# User session
def user_menu(username):
    print(WELCOME_COMMAND + username)
    print(OPTIONS_COMMAND)
    while True:
        option = input(username + " > ")
        if option == LOGOUT_COMMAND:
            print(LOGGING_OUT_COMMAND)
            break
        elif option == EXPENSES_COMMAND:
            expenses_menu(username)
        else:
            print(option + NOT_OPTION_COMMAND)


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
            print(CHOOSE_CORRECT_NUMBER_COMMAND)


def view_by_time_choice(username):
    choice_menu = {
        VIEW_BY_DATE_COMMAND: (view_by_day, ENTER_THE_DATE_COMMAND + "(YYYY-MM-DD)\n"),
        VIEW_BY_MONTH_COMMAND: (view_by_month, ENTER_THE_DATE_COMMAND + "(YYYY-MM)\n"),
        VIEW_BY_YEAR_COMMAND: (view_by_year, ENTER_THE_DATE_COMMAND + "(YYYY)\n")
    }
    time_choice = input(ENTER_THE_TIME_CHOICE_COMMAND)
    if time_choice in choice_menu:
        date = input(choice_menu[time_choice][1])
        print(choice_menu[time_choice][0](username, date))

    else:
        print(CHOOSE_CORRECT_NUMBER_COMMAND)


def view_by_certain_category_choice(username):
    category = input(ENTER_THE_CATEGORY_TO_SHOW_INFO_COMMAND)
    print(view(username, category))


def view_user_expenses_choice(username):
    print(view(username, category=None))


def insert_expenses_choice(username):
    amount = input(ENTER_THE_AMOUNT_COMMAND)
    category = input(ENTER_THE_CATEGORY_COMMAND)
    message = input(ENTER_THE_INFORMATION_COMMAND)
    date = input(ENTER_THE_DATE_COMMAND + ENTER_THE_DATE_OR_LEAVE_BLANK_FIELD_COMMAND)
    insert_expenses(username, amount, category, message, date)
