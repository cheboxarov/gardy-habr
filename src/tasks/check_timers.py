import time
from datetime import datetime
from db import session
from models import Timer
import settings


def check_timers(bot):
    while True:
        current_time = datetime.utcnow()
        timers = (
            session.query(Timer)
            .filter(Timer.end_time < current_time, Timer.discount_applied == False)
            .all()
        )

        for timer in timers:
            order = timer.order
            if order.status == "Finished" or order.status == "Rejected":
                timer.discount_applied = True
                session.commit()
                continue
            user = order.user
            user.has_promo = True

            session.commit()

            discount = settings.PROMO_PERCENT
            bot.send_message(
                user.user_id,
                f"Ваш заказ №{order.id} просрочен. Вы получили скидку {discount}% на следующий заказ.",
            )

            timer.discount_applied = True
            session.commit()

        time.sleep(60)  # Проверка каждые 60 секунд
