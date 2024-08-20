from models import User, Order
import settings


def order_text(user: User, order: Order, order_status: str = None, username: str = None) -> str:
    if order_status is None:
        if order.status == "Working":
            order_status = "В работе"
        if order.status == "Pending":
            order_status = "На рассмотрении"
        if order.status == "Finished":
            order_status = "Готов"
        if order.status == "Rejected":
            order_status = "Отклонен"
        if order.status == "Accepted":
            order_status = "Принят"
    if order_status is not None:
        order_status_text = f"""
💡*Статус заказа* 
┗ {order_status}"""
    else:
        order_status_text = ""
    text = f"""🧾 *Информация о заказе*
➖➖➖➖➖➖➖➖➖➖➖
📋 *Категория:* {order.category.name}
🌏 *Описание:* {order.description}
⏱️ *Срок выполнения:* {order.deadline}
➖➖➖➖➖➖➖➖➖➖➖
💰 *Цена: * {order.price}
🔖* Айди заказа: * {order.id}
🎯 *Персональная скидка:*
➖➖➖➖➖➖➖➖➖➖➖
{order_status_text}
——————————————————
Для обсуждения вопроса обратитесь к @gardy82"""
    if username is not None:
        return f"Заказ от @{username}\n{text}"
    return text
