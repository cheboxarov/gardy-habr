from telebot import types, TeleBot

from db import session
from models import Category


def handle_menu(bot: TeleBot, call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="welcome"))
    if call.data == "support":
        bot.edit_message_caption(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            caption="Для поддержки свяжитесь с нами: @gardyy00",
            reply_markup=markup,
        )
    elif call.data == "rules":
        bot.edit_message_caption(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            caption="Здесь будут указаны правила.",
            reply_markup=markup,
        )
    elif call.data == "portfolio":
        categories = session.query(Category).all()
        markup = types.InlineKeyboardMarkup()
        for category in categories:
            markup.add(
                types.InlineKeyboardButton(category.name, url=category.portfolio)
            )
        markup.add(types.InlineKeyboardButton("Назад", callback_data="welcome"))
        bot.edit_message_caption(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            caption="Портфолио",
            parse_mode="Markdown",
            reply_markup=markup,
        )
    elif call.data == "price":
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Сделать заказ", callback_data="make_order")
        )
        markup.add(types.InlineKeyboardButton("Назад", callback_data="welcome"))
        bot.edit_message_caption(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            caption="тут прайсы",
            reply_markup=markup,
        )
