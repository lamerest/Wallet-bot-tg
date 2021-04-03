from db import insert_transaction, delete_transaction, \
    look_budget, change_budget, \
    last_6_transactions, select_transaction
import datetime


def new_transaction(message):
    # Forming new query to insert it to db and calling change of budget
    # because of new transaction

    transaction = parse_message(message)
    
    if message[0] == "+":
        insert_transaction(transaction)
        change_budget(int(look_budget()[0]) + int(transaction[1]))
    else:
        insert_transaction(transaction)
        change_budget(int(look_budget()[0]) - int(transaction[1]))


def cancel_transaction(num):
    # Forming new query to delete transaction from db and calling change of budget
    # because of cancelling transaction
    deleting_transaction = select_transaction(num)
    delete_transaction(deleting_transaction[0])

    if deleting_transaction[1] == "+":
        total = int(look_budget()[0]) - deleting_transaction[2]
        change_budget(total)
    else:
        total = int(look_budget()[0]) + deleting_transaction[2]
        change_budget(total)

    return deleting_transaction


def month_expanses():
    expanses = 0
    return expanses


def check_budget() -> tuple:
    # Forming answer about current budget

    budget = look_budget()
    return budget


def last_operations() -> list:
    # Viewing and returning last 6 transactions
    return last_6_transactions()


def parse_message(message) -> tuple:
    # Parsing information about new transaction
    if message[0] == "-":
        message = "–" + message[1:]

    parsed_string = str(message).lower().split(" ", maxsplit=1)
    return (parsed_string[0][0],
            parsed_string[0][1:],
            parsed_string[1],
            str(datetime.datetime.now()).split('.')[0])
