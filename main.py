from authorization import init_users, login, register




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