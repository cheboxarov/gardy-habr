import time
from datetime import datetime
from db import session
from models import Timer
import settings
import string
import random
from formating.order_text_formatter import order_text


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
            status_text = f"""_Время истекло, к сожалению я чуть чуть не успеваю сдать заказ в обговоренные сроки, но я уже заканчиваю работу, и уже скоро ты сможешь насладится результатом!_

*❤️В качестве компенсации ты получаешь промокод на скидку -{discount}% на следующий заказ:* {user.promo} """
            bot.send_message(
                user.user_id,
                order_text(user, order, order_status=status_text),
                parse_mode="Markdown",
            )

            timer.discount_applied = True
            session.commit()

        time.sleep(60)  # Проверка каждые 60 секунд
