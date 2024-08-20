from db import session
from models import Order, User
from formating import order_text


def finish_order_handler(bot, call):
    order_id = int(call.data.split("_")[-1])
    order = session.query(Order).filter_by(id=order_id).first()
    user = session.query(User).filter_by(user_id=call.from_user.id).first()
    bot.delete_message(call.from_user.id, call.message.id)
    if order:
        order.status = "Finished"
        session.commit()
        bot.send_message(
            order.user_id,
            order_text(user, order, order_status="_Ваш заказ готов! Я уже отправил готовый результат Вам в личные сообщения. _"),
            parse_mode="Markdown",
        )
        session.commit()
