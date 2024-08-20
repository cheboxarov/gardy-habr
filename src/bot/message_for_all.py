from db import session
from models import User, Order
from telebot import TeleBot, types
from telebot.types import Message
from formating import order_text

def message_for_all_handler(bot: TeleBot, message: Message):
    users = session.query(User).all()
    message_text = message.html_text
    message_text = message_text.replace("all ", "")
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        for user in users:
            try:
                bot.send_message(user.user_id, message_text, parse_mode="html")
            except:
                pass
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")