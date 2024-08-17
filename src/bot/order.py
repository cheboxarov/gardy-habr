from telebot import types
from models import Category
from db import session
import json


def handle_order(bot, call):
    categories = session.query(Category).all()
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        markup.add(
            types.InlineKeyboardButton(
                category.name, callback_data=f"make_order_{category.id}"
            )
        )
    bot.send_message(
        call.message.chat.id, "Выберите категорию заказа:", reply_markup=markup
    )
