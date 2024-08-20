from db import session
from models import User, Order
from telebot import TeleBot, types
from telebot.types import Message


def message_for_all_handler(bot: TeleBot, message: Message):
    users = session.query(User).all()
    if not message.photo:
        message_text = message.html_text
    else:
        message_text = message.html_caption
    message_text = message_text.replace("all ", "")
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()

    if user and user.is_admin:
        # If there is a photo, send the photo along with the text
        if message.photo:
            photo = message.photo[-1].file_id  # The best quality photo
            for user in users:
                try:
                    bot.send_photo(user.user_id, photo, caption=message_text, parse_mode="html")
                except Exception as e:
                    pass  # You can log the error here if needed
        else:
            for user in users:
                try:
                    bot.send_message(user.user_id, message_text, parse_mode="html")
                except Exception as e:
                    pass  # You can log the error here if needed
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к админ панели.")
