from main import bot, dp
from aiogram.types import Message
from config import admin_id, start_message

from business_logic import new_transaction, delete_transaction, \
    check_budget, month_expanses, last_operations, cancel_transaction

from tinkoff import portfolio_balance


async def send_to_admin(dp):
    # Sends admin a message about start of work

    text = "Bot has started work!"
    await bot.send_message(chat_id=admin_id, text=text)


def auth(func):
    # Auth function to deny access for the unknown users

    async def wrapper(message):
        if int(message['from']['id']) != int(admin_id):
            return await message.reply("Access denied!", reply="False")
        return await func(message)
    return wrapper


@dp.message_handler(commands=["start", "help"])
async def start(message: Message):
    # Just start message, nothing special

    await bot.send_message(chat_id=admin_id, text=start_message)


@dp.message_handler(commands=["view"])
async def view_transactions(message: Message):
    await budget_message()


@dp.message_handler(commands=["del1", "del2", "del3", "del4", "del5", "del6"])
async def delete(message: Message):
    deleted_transaction = cancel_transaction(int(message.text[4]))
    text = "Удалена операция: "
    date = "(" + str(deleted_transaction[4]).split(" ")[1] + "  " + str(deleted_transaction[4]).split(" ")[0] + ")"
    text += str(deleted_transaction[1]) + "" + str(deleted_transaction[2]) + "  " + str(deleted_transaction[3]) + "  " + date + "\n\n"
    await bot.send_message(chat_id=admin_id, text=text)
    await budget_message()


@dp.message_handler()
@auth
async def receiver(message: Message):
    # Receive most of messages, including messages with information about transactions
    # Checks message to see if it follows the rules
    # Answers about adding new transaction and sends current budget

    new_transaction(message.text)
    month_expanses()

    await budget_message()


async def budget_message():
    budget = check_budget()
    text = "Бюджет составляет:\n\n" + str(budget[0]) + " ₽" + "\n\nВаш брокерский счёт (Tinkoff):\n\n" + str(
        portfolio_balance()) + " ₽"
    text += "\n\nПоследние операции:\n\n"
    del_counter = 6
    for i in last_operations():
        date = "(" + str(i[4]).split(" ")[1] + "  " + str(i[4]).split(" ")[0] + ")"
        text += "/del" + str(del_counter) + "  " + str(i[1]) + "" + str(i[2]) + "  " + str(i[3]) + "  " + date + "\n\n"
        del_counter -= 1
    await bot.send_message(chat_id=admin_id, text=text)
