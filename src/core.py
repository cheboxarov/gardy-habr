import telebot
import os
from db import engine
import logging
from models import Base
import threading
from bot import (
    welcome_handler,
    start_order_handler,
    admin_new_orders,
    admin_manage_order_handler,
    handle_menu,
    handle_category_selection,
    create_order_handle,
    welcome_callback_handler,
    admin_accepted_orders,
    admin_panel_handler,
    finish_order_handler,
    orders_in_work,
    finished_orders,
    pend_order_handler,
    cancel_order_handler,
message_for_all_handler
)
from tasks.check_timers import check_timers
from telebot.types import CallbackQuery
from sqlalchemy.inspection import inspect
from db.core import create_tables

# Инициализация бота
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")


@bot.message_handler(commands=["start"])
def start_message(message):
    welcome_handler(bot, message)


@bot.callback_query_handler(func=lambda call: call.data == "welcome")
def start_message_callback(call):
    welcome_callback_handler(bot, call)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(
    func=lambda call: call.data in ["support", "rules", "portfolio", "price"]
)
def menu(call):
    handle_menu(bot, call)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == "make_order")
def order(call):
    create_order_handle(bot, call)
    bot.answer_callback_query(call.id, "")


@bot.callback_query_handler(func=lambda call: call.data.startswith("make_order_"))
def category_selection(call):
    handle_category_selection(bot, call)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("pend_order_"))
def category_selection(call):
    pend_order_handler(bot, call)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel_order_"))
def category_selection(call):
    cancel_order_handler(bot, call)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_work_"))
def accept_order(call):
    start_order_handler(bot, call)
    bot.answer_callback_query(call.id, "")


@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_finish_"))
def finish_order(call):
    finish_order_handler(bot, call)
    bot.answer_callback_query(call.id, "")


@bot.message_handler(commands=["admin"])
def admin_panel(message):
    admin_panel_handler(bot, message)


@bot.message_handler(commands=["new_orders"])
def admin_panel(message):
    admin_new_orders(bot, message)


@bot.message_handler(commands=["accepted_orders"])
def admin_panel(message):
    admin_accepted_orders(bot, message)


@bot.message_handler(commands=["work_orders"])
def admin_panel(message):
    orders_in_work(bot, message)


@bot.message_handler(commands=["finished_orders"])
def admin_panel(message):
    finished_orders(bot, message)


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("admin_accept_")
    or call.data.startswith("admin_reject_")
)
def admin_manage_order(call: CallbackQuery):
    admin_manage_order_handler(bot, call)
    bot.answer_callback_query(call.id, "")

@bot.message_handler(content_types=["text"], func=lambda message: message.text.startswith("all "))
def message_for_all(message):
    message_for_all_handler(bot, message)

@bot.message_handler(content_types=["text"])
def start_message(message):
    welcome_handler(bot, message)


if __name__ == "__main__":
    print("Creating tables...")
    create_tables()
    print("Tables created successfully!")

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(tables)

    timer_thread = threading.Thread(target=check_timers, args=(bot,))
    timer_thread.start()
    while True:
        try:
            bot.polling(none_stop=True, logger_level=logging.DEBUG)
        except Exception as error:
            print(error)
