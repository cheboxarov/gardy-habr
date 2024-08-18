import time
from datetime import datetime
from db import session
from models import Timer
import settings
import string
import random


def generate_unique_string(length=10):
    # Проверяем, чтобы длина не превышала доступные уникальные символы
    if length > len(string.ascii_letters + string.digits):
        raise ValueError("Requested length exceeds the number of unique characters available")

    characters = string.ascii_letters + string.digits
    # Генерируем уникальную строку
    return ''.join(random.sample(characters, length))
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
            user.promo = generate_unique_string()

            session.commit()

            discount = settings.PROMO_PERCENT
            bot.send_message(
                user.user_id,
                f"Ваш заказ №{order.id} просрочен. Вы получили промокод {user.promo} на скидку {discount}% на следующий заказ.",
                parse_mode="Markdown",
            )

            timer.discount_applied = True
            session.commit()

        time.sleep(60)  # Проверка каждые 60 секунд
