from db import session
from models import Order, User
from formating import order_text


def admin_manage_order_handler(bot, call):
    order_id = int(call.data.split("_")[-1])
    order = session.query(Order).filter_by(id=order_id).first()
    user = session.query(User).filter_by(user_id=call.from_user.id).first()
    if "accept" in call.data:
        order.status = "Accepted"
        bot.send_message(
            order.user_id,
            f"{order_text(user, order)}\n\n*Принят.* \n\nМы свяжемся с вами для дальнейшего обсуждения.",
            parse_mode="Markdown",
        )
    elif "reject" in call.data:
        order.status = "Rejected"
        bot.send_message(
            order.user_id,
            f"{order_text(user, order)}\n\n*Отклонен.* \n\nСвяжитесь с технической поддержкой.",
            parse_mode="Markdown",
        )

    session.commit()
