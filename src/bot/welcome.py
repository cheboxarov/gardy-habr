from db import session
from models import User
from telebot import types, TeleBot


def welcome_handler(bot: TeleBot, message):
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        user = User(
            user_id=user_id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        session.add(user)
        session.commit()

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🛠 Техподдержка", callback_data="support"),
        types.InlineKeyboardButton("📜 Правила", callback_data="rules"),
    )
    markup.add(
        types.InlineKeyboardButton("🎨 Портфолио", callback_data="portfolio"),
        types.InlineKeyboardButton("💰 Прайс", callback_data="price"),
    )

    markup.add(
        types.InlineKeyboardButton("💰 Сделать заказ", callback_data="make_order")
    )

    bot.send_photo(
        message.chat.id,
        photo=open("imgs/test.jpg", "rb").read(),
        caption=f"Привет, {message.from_user.first_name}! Добро пожаловать!",
        reply_markup=markup,
    )


def welcome_callback_handler(bot: TeleBot, call):
    user_id = call.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        user = User(
            user_id=user_id,
            username=call.from_user.username,
            full_name=call.from_user.full_name,
        )
        session.add(user)
        session.commit()

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🛠 Техподдержка", callback_data="support"),
        types.InlineKeyboardButton("📜 Правила", callback_data="rules"),
    )
    markup.add(
        types.InlineKeyboardButton("🎨 Портфолио", callback_data="portfolio"),
        types.InlineKeyboardButton("💰 Прайс", callback_data="price"),
    )

    markup.add(
        types.InlineKeyboardButton("💰 Сделать заказ", callback_data="make_order")
    )

    bot.edit_message_caption(
        chat_id=call.from_user.id,
        message_id=call.message.id,
        caption=f"Привет, {call.from_user.first_name}! Добро пожаловать!",
        reply_markup=markup,
    )
