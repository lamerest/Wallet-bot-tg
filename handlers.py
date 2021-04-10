from main import bot, dp
from aiogram.types import Message
from config import admin_id, start_message

from business_logic import new_transaction, \
    check_budget, last_operations, cancel_transaction, uncategory_expanse, check_date

from db import view_category_expanses, number_of_operations

# from tinkoff import portfolio_balance


def auth(func):
    # Auth function to deny access for the unknown users

    async def wrapper(message):
        if int(message['from']['id']) != int(admin_id) and int(message['from']['id']) != 778838589:
            return await message.reply("Access denied!", reply="False")
        return await func(message)
    return wrapper


async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Bot started work...")


@dp.message_handler(commands=["start", "help"])
async def start(message: Message):
    # Just start message, nothing special

    await bot.send_message(chat_id=message.from_user.id, text=start_message)


@dp.message_handler(commands=["view"])
@auth
async def view_transactions(message: Message):
    check_date()
    await budget_message(message)


@dp.message_handler(commands=["del1", "del2", "del3", "del4", "del5", "del6"])
@auth
async def delete(message: Message):
    deleted_transaction = cancel_transaction(int(message.text[4]))
    uncategory_expanse(deleted_transaction)
    text = "Удалена операция: "
    date = "(" + str(deleted_transaction[4]).split(" ")[1] + "  " + str(deleted_transaction[4]).split(" ")[0] + ")"
    text += str(deleted_transaction[1]) + "" + str(deleted_transaction[2]) + "  " + str(deleted_transaction[3]) + "  " + date + "\n\n"
    await bot.send_message(chat_id=message.from_user.id, text=text)
    await budget_message(message)


@dp.message_handler(commands=["month"])
@auth
async def month_stats(message: Message):
    check_date()
    expanses = view_category_expanses()
    text = "Траты за месяц по категориям:\n\n"
    for category in expanses:
        text = text + str(category[0]) + " - " + str(category[1]) + " ₽" + "\n\n"
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler()
@auth
async def receiver(message: Message):
    # Receive most of messages, including messages with information about transactions
    # Checks message to see if it follows the rules
    # Answers about adding new transaction and sends current budget
    if (message.text[0] == "+" or message.text[0] == "-") and " " in message.text:
        try:
            if isinstance(int(str(str(message.text).split(" ", maxsplit=1)[0])[1:]), int):
                new_transaction(message.text)
                await budget_message(message)
        except ValueError:
            pass
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Are u gay?")


async def budget_message(message):
    budget = check_budget()
    text = "Бюджет составляет:\n\n" + str(budget[0]) + " ₽"
    # "\n\nВаш брокерский счёт (Tinkoff):\n\n" + str(
    # portfolio_balance()) + " ₽"
    text += "\n\nПоследние операции:\n\n"
    if number_of_operations() >= 6:
        del_counter = 6
    else:
        del_counter = number_of_operations()
    for i in last_operations():
        date = "(" + str(i[4]).split(" ")[1] + "  " + str(i[4]).split(" ")[0] + ")"
        text += "/del" + str(del_counter) + "  " + str(i[1]) + "" + str(i[2]) + "  " + str(i[3]) + "  " + date + "\n\n"
        del_counter -= 1
    await bot.send_message(chat_id=message.from_user.id, text=text)
