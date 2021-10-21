import sqlite3 as db
from datetime import datetime

def init():
    conn = db.connect("main.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string
        )   
    '''
    cur.execute(sql)
    conn.commit()

def insert_info(amount, category, message="", date=None):

    if date == None:
        date = str(datetime.now().strftime("%Y-%m-%d"))
    data = (amount, category, message, date)
    conn = db.connect("main.db")
    cur = conn.cursor()
    sql = 'INSERT INTO expenses VALUES (?, ?, ?, ?)'
    cur.execute(sql, data)
    conn.commit()


def delete_info():
    conn = db.connect("main.db")
    cur = conn.cursor()
    sql = 'DELETE FROM expenses'
    cur.execute(sql)
    conn.commit()

# log(120, "transport", "uber to the home")

def view(category=None):
    conn = db.connect("main.db")
    cur = conn.cursor()
    if category:
        sql = '''
        select * from expenses where category = '{}'
        '''.format(category)

        sql2 = '''
        select sum(amount) from expenses where category = '{}'
        '''.format(category)

    else:
        sql = '''
        select * from expenses 
        '''.format(category)

        sql2 = '''
        select sum(amount) from expenses 
        '''.format(category)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]

    return total_amount, results


def view_by_time(date=None):
    conn = db.connect("main.db")
    cur = conn.cursor()
    if date:
        sql = '''
        select * from expenses where date = '{}'
        '''.format(date)

        sql2 = '''
        select sum(amount) from expenses where date = '{}'
        '''.format(date)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results


def view_by_month(date=None):
    conn = db.connect("main.db")
    cur = conn.cursor()
    if date:
        sql = '''
            select * from expenses where strftime('%Y-%m', date) = '{}';
            '''.format(date)
        sql2 = '''
            select sum(amount) from expenses where strftime('%Y-%m', date) = '{}';
            '''.format(date)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results


def view_by_year(date=None):
    conn = db.connect("main.db")
    cur = conn.cursor()
    if date:
        sql = '''
            select * from expenses where strftime('%Y', date) = '{}';
            '''.format(date)
        sql2 = '''
            select sum(amount) from expenses where strftime('%Y', date) = '{}';
            '''.format(date)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results

# insert_info(120, 'transport', 'uber to home')
# insert_info(150, 'food', 'pizza for homies')
# print(view('food'))
#
# print(view())

def main():

    # init()

    choice = input("Enter number 1, 2, 3, 4, 5, 6\n")
    if choice == "1":
        amount = input("Enter the amount\n")
        category = input("Enter the category\n")
        message = input("Enter the information\n")
        date = input("Enter the date\n")
        insert_info(amount, category, message, date)

    if choice == "2":
        print(view())

    if choice == "3":
        category = input("Enter the category to show info\n")
        print(view(category))

    if choice == "4":
        delete_info()

    if choice == "5":
        time_choice = input("Enter 1, 2, 3\n")
        if time_choice == "1":
            date = input("Enter the date\n")
            print(view_by_time(date))

        if time_choice == "2":
            date = input("Month\n")
            print(view_by_month(date))

        if time_choice == "3":
            date = input("Year\n")
            print(view_by_year(date))


main()
