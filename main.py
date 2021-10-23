from authorization import init_users, login, register
from settings import LOGIN_COMMAND, REGISTER_COMMAND, EXIT_FROM_PROGRAM_COMMAND


def start():
    init_users()
    # On start
    print("Welcome to the system. Please register or login.")
    print("Options: register | login | exit")
    while True:
        option = input("> ")
        if option == LOGIN_COMMAND:
            login()
        elif option == REGISTER_COMMAND:
            register()
        elif option == EXIT_FROM_PROGRAM_COMMAND:
            # On exit
            print("Shutting down...")
            break
        else:
            print(option + " is not an option")


if __name__ == '__main__':
    start()
