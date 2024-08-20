from db import session
from models import User
from telebot import types, TeleBot
from models import Order

def get_welcome_text(username: str) -> str:
    work_orders = session.query(Order).filter(Order.status=="Working").all()
    finished_orders = session.query(Order).filter(Order.status=="Finished").all()
    return f"""
    👋🏼 *Добро пожаловать* «{username}», это *Service Gardy*. Тут ты можешь заказать *дизайн* и другие *услуги*.
➖➖➖➖➖➖➖➖➖➖➖
💫 Количество выполненных заказов: {711+len(finished_orders)}
🖌️ Заказов в работе: {len(work_orders)}
ℹ️ *Чтобы узнать больше, сделать заказ используй кнопки ниже*"""

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

    send_welcome_message(bot, user_id, message.from_user.full_name)


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
    send_welcome_message(bot, user_id, call.from_user.full_name, call.message.id)

def send_welcome_message(bot, user_id: int, user_full_name: str, message_id: int = None):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📱Контакт для связи", callback_data="support"),
        types.InlineKeyboardButton("📜 Правила", callback_data="rules"),
    )
    markup.add(
        types.InlineKeyboardButton("🎨 Портфолио", callback_data="portfolio"),
        types.InlineKeyboardButton("💰 Прайс", callback_data="price"),
    )

    markup.add(
        types.InlineKeyboardButton("💰 Сделать заказ", callback_data="make_order")
    )

    if message_id:
        bot.edit_message_caption(
            chat_id=user_id,
            message_id=message_id,
            caption=get_welcome_text(user_full_name),
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_photo(
            user_id,
            photo=open("imgs/test.jpg", "rb").read(),
            caption=get_welcome_text(user_full_name),
            reply_markup=markup,
            parse_mode="Markdown",
        )