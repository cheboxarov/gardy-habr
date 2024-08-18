from models import User, Order
import settings


def order_text(user: User, order: Order) -> str:
    text = f"Заказ №{order.id}\nОт @{order.user.username}\nКатегория: {order.category.name}\nОписание: {order.description}\nЦена: {order.price} руб.\nДедлайн: {order.deadline}"
    return text
