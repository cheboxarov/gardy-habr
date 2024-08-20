from telebot import types
import settings
from db import session
from models import User, Order
from formating import order_text


def admin_panel_handler(bot, message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.InlineKeyboardButton("/new_orders"))
        markup.add(types.InlineKeyboardButton("/accepted_orders"))
        markup.add(types.InlineKeyboardButton("/work_orders"))
        markup.add(types.InlineKeyboardButton("/finished_orders"))
        bot.send_message(user_id, "Админка", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")


def admin_new_orders(bot, message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        orders = session.query(Order).filter_by(status="Pending").all()
        if orders:
            for order in orders:
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(
                        "Принять", callback_data=f"admin_accept_{order.id}"
                    )
                )
                markup.add(
                    types.InlineKeyboardButton(
                        "Отклонить", callback_data=f"admin_reject_{order.id}"
                    )
                )
                bot.send_message(
                    message.chat.id,
                    order_text(user, order, username=user.username),
                    reply_markup=markup,
                )
        else:
            bot.send_message(message.chat.id, "Нет новых заказов.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")


def admin_accepted_orders(bot, message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        orders = session.query(Order).filter_by(status="Accepted").all()
        if orders:
            for order in orders:
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(
                        "Взять в работу", callback_data=f"admin_work_{order.id}"
                    )
                )
                markup.add(
                    types.InlineKeyboardButton(
                        "Отклонить", callback_data=f"admin_reject_{order.id}"
                    )
                )
                bot.send_message(
                    message.chat.id,
                    order_text(user, order, username=user.username),
                    reply_markup=markup,
                )
        else:
            bot.send_message(message.chat.id, "Нет принятых заказов.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")


def orders_in_work(bot, message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        orders = session.query(Order).filter_by(status="Working").all()
        if orders:
            for order in orders:
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton(
                        "Выполнить", callback_data=f"admin_finish_{order.id}"
                    )
                )
                markup.add(
                    types.InlineKeyboardButton(
                        "Отклонить", callback_data=f"admin_reject_{order.id}"
                    )
                )
                bot.send_message(
                    message.chat.id,
                    order_text(user, order, username=user.username),
                    reply_markup=markup,
                )
        else:
            bot.send_message(message.chat.id, "Нет заказов в работе.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")


def finished_orders(bot, message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        orders = session.query(Order).filter_by(status="Finished").all()
        if orders:
            for order in orders:
                markup = types.InlineKeyboardMarkup()
                bot.send_message(
                    message.chat.id,
                    order_text(user, order, username=user.username),
                    reply_markup=markup,
                )
        else:
            bot.send_message(message.chat.id, "Нет завершенных заказов.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")
