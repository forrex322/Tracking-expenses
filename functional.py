import sqlite3 as db
from datetime import datetime
from settings import DATABASE_NAME

def init_db():
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses (
        amount number,
        category string,
        message string,
        date string,
        user_id integer,
        FOREIGN KEY (user_id)
            REFERENCES users (user_id)
        )   
    '''
    cur.execute(sql)
    conn.commit()


def insert_expenses(username, amount, category, message="", date=""):
    if not date:
        date = str(datetime.now().strftime("%Y-%m-%d"))
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    data = (int(current_user_id), amount, category, message, date)
    sql = 'insert into expenses (user_id, amount, category, message, date) values (?, ?, ?, ?, ?)'

    cur.execute(sql, data)
    conn.commit()


def delete_user_expenses(username):
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    sql = 'delete from expenses where user_id = "{}"'.format(current_user_id)

    cur.execute(sql)
    conn.commit()


def view(username, category=None):
    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    if category:
        sql = '''
        select * from expenses where category = '{}' and user_id = '{}'
        '''.format(category, current_user_id)

        sql2 = '''
        select sum(amount) from expenses where category = '{}' and user_id = '{}'
        '''.format(category, current_user_id)

    else:
        sql = '''
        select * from expenses where user_id = '{}'
        '''.format(current_user_id)

        sql2 = '''
        select sum(amount) from expenses where user_id = '{}'
        '''.format(current_user_id)

    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results


def view_by_day(username, date=None):
    return view_by_date(username, date, "%Y-%m-%d")


def view_by_month(username, date=None):
    return view_by_date(username, date, "%Y-%m")


def view_by_year(username, date=None):
    return view_by_date(username, date, "%Y")


def view_by_date(username, date=None, date_format="%Y-%m"):

    conn = db.connect(DATABASE_NAME)
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    if date:
        sql = '''
                select * from expenses where strftime('{}', date) = '{}' and user_id = '{}';
                '''.format(date_format, date, current_user_id)
        sql2 = '''
                select sum(amount) from expenses where strftime('{}', date) = '{}' and user_id = '{}';
                '''.format(date_format, date, current_user_id)

    print(sql)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results