import sqlite3

# Here is all the functions that sending queries to the db


def insert_transaction(entries):
    # Inserts new transaction into the db

    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO transactions(action, sum, category, datetime) VALUES(?, ?, ?, ?)", entries)
    db.commit()
    db.close()


def delete_transaction(identifier):
    # Deletes chosen transaction from db

    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM transactions WHERE id = {identifier}")
    db.commit()
    db.close()


def look_budget() -> tuple:
    # Checks budget's numbers

    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM budget")
    budget = cursor.fetchone()
    db.commit()
    db.close()
    return budget


def change_budget(total):
    # Changes budget numbers

    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE budget SET total = {total}")
    db.commit()
    db.close()


def last_6_transactions():
    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()[len(cursor.fetchmany()) - 6:]
    db.commit()
    db.close()
    return transactions


def select_transaction(num):
    # Selects one of 6 last transactions

    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM transactions")
    transaction = cursor.fetchall()[len(cursor.fetchmany()) - num]
    db.commit()
    db.close()
    return transaction


def show_month_expanses():
    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute("SELECT name, month_expanses FROM category")
    expanses = cursor.fetchall()
    db.commit()
    db.close()
    return expanses


def update_category_expanse(codename, total):
    # Updates total expanses for given category

    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE category SET month_expanses = {total} WHERE codename = {codename}")
    db.commit()
    db.close()


def check_category_expanses(aliase):
    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM transactions")
    transaction = cursor.fetchall()[len(cursor.fetchmany()) - num]
    db.commit()
    db.close()


def get_aliases():
    db = sqlite3.connect("finance.db")
    cursor = db.cursor()
    cursor.execute("SELECT codename, aliases FROM category")
    aliases = cursor.fetchall()
    db.commit()
    db.close()
    return aliases
