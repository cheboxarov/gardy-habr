from db import session
from models import Order, Timer, User
from datetime import datetime, timedelta
from formating import order_text


def start_order_handler(bot, call):
    order_id = int(call.data.split("_")[-1])
    order = session.query(Order).filter_by(id=order_id).first()
    user = session.query(User).filter_by(user_id=call.from_user.id).first()
    if order:
        order.status = "Working"
        session.commit()
        bot.send_message(
            order.user_id,
            f"{order_text(user, order)} \n\n*Взят в работу.*",
            parse_mode="Markdown",
        )

        # Установка таймера на выполнение заказа
        end_time = datetime.utcnow() + timedelta(
            hours=order.deadline_hours
        )  # например, 24 часа на выполнение
        timer = Timer(order_id=order.id, end_time=end_time)
        session.add(timer)
        session.commit()
