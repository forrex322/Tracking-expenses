import sqlite3 as db
from datetime import datetime
import time


def init_db():
    conn = db.connect("main.db")
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


def insert_expenses(username, amount, category, message="", date=None):
    if date == "":
        date = str(datetime.now().strftime("%Y-%m-%d"))
    conn = db.connect("main.db")
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    data = (int(current_user_id), amount, category, message, date)
    sql = 'insert into expenses (user_id, amount, category, message, date) values (?, ?, ?, ?, ?)'

    cur.execute(sql, data)
    conn.commit()


def delete_info(username):
    conn = db.connect("main.db")
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    sql = 'delete from expenses where user_id = "{}"'.format(current_user_id)

    cur.execute(sql)
    conn.commit()


def view(username, category=None):
    conn = db.connect("main.db")
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


def view_by_time(username, date=None):
    conn = db.connect("main.db")
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    if date:
        sql = '''
        select * from expenses where date = '{}' and user_id = '{}'
        '''.format(date, current_user_id)

        sql2 = '''
        select sum(amount) from expenses where date = '{}' and user_id = '{}'
        '''.format(date, current_user_id)

    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results


def view_by_month(username, date=None):
    conn = db.connect("main.db")
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    if date:
        sql = '''
            select * from expenses where strftime('%Y-%m', date) = '{}' and user_id = '{}';
            '''.format(date, current_user_id)
        sql2 = '''
            select sum(amount) from expenses where strftime('%Y-%m', date) = '{}' and user_id = '{}';
            '''.format(date, current_user_id)

    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results


def view_by_year(username, date=None):
    conn = db.connect("main.db")
    cur = conn.cursor()

    cur.execute("select user_id from users where username = ?", (username,))
    current_user_id = cur.fetchone()[0]
    if date:
        sql = '''
            select * from expenses where strftime('%Y', date) = '{}' and user_id = '{}';
            '''.format(date, current_user_id)
        sql2 = '''
            select sum(amount) from expenses where strftime('%Y', date) = '{}' and user_id = '{}';
            '''.format(date, current_user_id)

    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return total_amount, results
