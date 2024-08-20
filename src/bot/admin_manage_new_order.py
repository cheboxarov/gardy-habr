from db import session
from models import Order, User
from formating import order_text
from telebot import TeleBot


def admin_manage_order_handler(bot: TeleBot, call):
    order_id = int(call.data.split("_")[-1])
    order = session.query(Order).filter_by(id=order_id).first()
    user = session.query(User).filter_by(user_id=call.from_user.id).first()
    bot.delete_message(call.from_user.id, call.message.id)
    if "accept" in call.data:
        order.status = "Accepted"
        bot.send_message(
            order.user_id,
            order_text(user, order, order_status="_Ваш заказ принят, я скоро свяжусь с вами._"),
            parse_mode="Markdown",
        )
    elif "reject" in call.data:
        order.status = "Rejected"
        bot.send_message(
            order.user_id,
            order_text(user, order, order_status="_Ваш заказ отклонен, свяжитесь с технической поддержкой_"),
            parse_mode="Markdown",
        )

    session.commit()
