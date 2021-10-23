from authorization import init_users, login, register
from settings import LOGIN_COMMAND, REGISTER_COMMAND, EXIT_FROM_PROGRAM_COMMAND, WELCOME_MENU_COMMAND, \
    OPTIONS_MENU_COMMAND, SHUT_DOWN_COMMAND, NOT_OPTION_COMMAND


def start():
    init_users()
    # On start
    print(WELCOME_MENU_COMMAND)
    print(OPTIONS_MENU_COMMAND)
    while True:
        option = input("> ")
        if option == LOGIN_COMMAND:
            login()
        elif option == REGISTER_COMMAND:
            register()
        elif option == EXIT_FROM_PROGRAM_COMMAND:
            # On exit
            print(SHUT_DOWN_COMMAND)
            break
        else:
            print(option + NOT_OPTION_COMMAND)


if __name__ == '__main__':
    start()
