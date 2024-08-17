from db import session
from models import Order, User
from formating import order_text


def finish_order_handler(bot, call):
    order_id = int(call.data.split("_")[-1])
    order = session.query(Order).filter_by(id=order_id).first()
    user = session.query(User).filter_by(user_id=call.from_user.id).first()
    if order:
        order.status = "Finished"
        session.commit()
        bot.send_message(
            order.user_id,
            f"{order_text(user, order)} \n\n*Завершен.*",
            parse_mode="Markdown",
        )
        session.commit()
