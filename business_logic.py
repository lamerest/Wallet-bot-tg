from db import insert_transaction, delete_transaction, \
    look_budget, change_budget, \
    last_6_transactions, select_transaction, \
    get_aliases, \
    check_category_expanses, update_category_expanse, view_category_expanses, \
    insert_month_expanses, last_date, clear_month_expanses, clear_transactions
import datetime


def new_transaction(message):
    # Forming new query to insert it to db and calling change of budget
    # because of new transaction
    check_date()
    transaction = parse_message(message)

    if message[0] == "+":
        insert_transaction(transaction)
        change_budget(int(look_budget()[0]) + int(transaction[1]))
    else:
        category_expanse(transaction)
        insert_transaction(transaction)
        change_budget(int(look_budget()[0]) - int(transaction[1]))


def cancel_transaction(num):
    # Forming new query to delete transaction from db and calling change of budget
    # because of cancelling transaction
    canceled_transaction = select_transaction(num)
    delete_transaction(canceled_transaction[0])

    if canceled_transaction[1] == "+":
        total = int(look_budget()[0]) - canceled_transaction[2]
        change_budget(total)
    else:
        total = int(look_budget()[0]) + canceled_transaction[2]

        change_budget(total)

    return canceled_transaction


def check_budget() -> tuple:
    # Forming answer about current budget

    budget = look_budget()
    return budget


def last_operations() -> list:
    # Viewing and returning last 6 transactions
    return last_6_transactions()


def category_expanse(transaction):
    categories = get_aliases()
    transaction_category = ""
    for category in categories:
        if transaction[2] in category[1]:
            transaction_category = category[0]
            break

    if not transaction_category:
        transaction_category = "other"

    total = check_category_expanses(transaction_category) + int(transaction[1])
    update_category_expanse(transaction_category, total)


def uncategory_expanse(transaction):
    categories = get_aliases()
    transaction_category = ""
    for category in categories:
        if transaction[3] in category[1]:
            transaction_category = category[0]
            break

    if not transaction_category:
        transaction_category = "other"

    total = check_category_expanses(transaction_category) - int(transaction[2])
    update_category_expanse(transaction_category, total)


def check_date():
    last_operation_date = last_date()
    date_now = str(datetime.datetime.now().year) + " " + str(datetime.datetime.now().month)
    if last_operation_date != date_now:
        print("Запущена месячная очистка!")
        print(last_operation_date, date_now)
        data = []
        for category in view_category_expanses():
            data.append(category[1])
        data.append(last_operation_date)
        insert_month_expanses(data)
        clear_month_expanses()
        clear_transactions()


def parse_message(message) -> tuple:
    # Parsing information about new transaction
    if message[0] == "-":
        message = "–" + message[1:]

    parsed_string = str(message).lower().split(" ", maxsplit=1)
    return (parsed_string[0][0],
            parsed_string[0][1:],
            parsed_string[1],
            str(datetime.datetime.now()).split('.')[0])
