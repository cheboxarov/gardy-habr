from telebot import types
from models import Category
from db import session
import json
from models import User, Order
from telebot import TeleBot


def create_order_handle(bot: TeleBot, call):
    user_id = call.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    order_exists = (
            session.query(Order)
            .filter(Order.user_id == user_id, Order.status == "Pending")
            .limit(1)
            .scalar()
            is not None
    )
    if order_exists:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Вернуться в меню", callback_data="welcome")
        )
        bot.edit_message_caption(
            chat_id=user_id,
            message_id=call.message.id,
            caption="Вы уже оставляли заказ, он находится на рассмотрении, подождите немного.",
            reply_markup=markup,
        )
        return
    categories = session.query(Category).filter(Category.parent_id.is_(None)).all()
    markup = types.InlineKeyboardMarkup()
    for category in categories:
        markup.add(
            types.InlineKeyboardButton(
                category.name, callback_data=f"make_order_{category.id}"
            )
        )
    bot.send_message(
        call.message.chat.id, """*Выберите категорию товара. *
❔_Если вы не можете определиться  с нужной для вас категорией, напишите мне в лс:_ @Gardy82""", reply_markup=markup
    )
