from telebot import types, TeleBot
from .utils.menu_utils import get_pricing_text
from db import session
from models import Category


def handle_menu(bot: TeleBot, call: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Назад", callback_data="welcome"))
    if call.data == "support":
        bot.edit_message_caption(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            caption="""
            🫱🏽‍🫲🏼*По всем вопросам вы можете обратиться напрямую ко мне: @Gardy82*""",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    elif call.data == "rules":
        bot.edit_message_caption(
            chat_id=call.from_user.id,
            message_id=call.message.id,
            caption="Здесь будут указаны правила.",
            reply_markup=markup,
        )
    elif call.data == "portfolio":
        categories = session.query(Category).filter(Category.parent_id.is_(None)).all()
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Основное портфолио", url="https://t.me/+4Ty_2eBSsXg5MDUy"))
        for category in categories:
            if category.portfolio is not None:
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
            caption=get_pricing_text(),
            reply_markup=markup,
            parse_mode="Markdown"
        )
