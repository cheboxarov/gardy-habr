from telebot import types
from models import Order, User, Category, Price
from db import session
from telebot import TeleBot
from formating import order_text
from .welcome import welcome_handler


def pend_order_handler(bot: TeleBot, call):
    order_id = call.data.split("_")[-1]
    order = (
        session.query(Order).filter_by(id=order_id, user_id=call.from_user.id).first()
    )
    if order is None:
        return
    order.status = "Pending"
    session.commit()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Вернуться в меню", callback_data="welcome"))

    bot.edit_message_caption(
        chat_id=call.from_user.id,
        message_id=call.message.id,
        caption=f"Ваш заказ отправлен на модерацию, ожидайте.",
        reply_markup=markup,
    )
    admin_users = session.query(User).filter(User.is_admin == True).all()
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Принять", callback_data=f"accept_order_{order.id}")
    )
    for user in admin_users:
        bot.send_message(
            user.user_id,
            f"{call.from_user.username} оформил заказ.\n\n{order_text(order.user, order)}",
        )


def cancel_order_handler(bot: TeleBot, call):
    order_id = call.data.split("_")[-1]
    order = (
        session.query(Order).filter_by(id=order_id, user_id=call.from_user.id).first()
    )
    if order is None:
        return
    order.status = "Canceled"
    session.commit()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Вернуться в меню", callback_data="welcome"))

    bot.edit_message_caption(
        chat_id=call.from_user.id,
        message_id=call.message.id,
        caption=f"Ваш заказ отменен.",
        reply_markup=markup,
    )


def get_order_details(bot: TeleBot, message, context):
    category = context["category"]
    price = context["price"]
    description = message.text
    deadline = context["deadline"]
    deadline_hours = 24
    if deadline == "Сегодня (+ %100 от заказа)":
        deadline_hours = 12
    if deadline == "Сутки (+ %50 от заказа)":
        deadline_hours = 24
    if deadline == "2 дня (+ %15 от заказа)":
        deadline_hours = 48
    if deadline == "2-4 дня":
        deadline_hours = 96
    user_id = message.from_user.id
    user = session.query(User).filter_by(user_id=user_id).first()
    order_exists = (
        session.query(Order)
        .filter(Order.user_id == user_id, Order.status == "Pending")
        .limit(1)
        .scalar()
        is not None
    )
    if order_exists:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Вернуться в меню", callback_data="welcome")
        )
        bot.send_photo(
            message.chat.id,
            photo=open("imgs/test.jpg", "rb").read(),
            caption="Вы уже оставляли заказ, он находится на рассмотрении, подождите немного.",
            reply_markup=markup,
        )
        return
    username = message.from_user.username
    order = Order(
        user_id=user_id,
        category_id=category.id,
        description=description,
        price=price,
        status="Created",
        deadline=deadline,
        deadline_hours=deadline_hours,
    )
    session.add(order)
    session.commit()

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Подтвердить", callback_data=f"pend_order_{order.id}"
        )
    )
    markup.add(
        types.InlineKeyboardButton("Отменить", callback_data=f"cancel_order_{order.id}")
    )
    markup.add(types.InlineKeyboardButton("Вернуться в меню", callback_data="welcome"))

    bot.send_photo(
        message.chat.id,
        photo=open("imgs/test.jpg", "rb").read(),
        caption=f"Ваш заказ:\n\n{order_text(user, order)}",
        reply_markup=markup,
    )


def get_order_deadline(bot: TeleBot, message, context):
    if not message.text in [
        "Сегодня (+ %100 от заказа)",
        "Сутки (+ %50 от заказа)",
        "2 дня (+ %15 от заказа)",
        "2-4 дня"
    ]:
        message = bot.send_message(
            message.from_user.id,
            f"Вы указали неправильное время.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        welcome_handler(bot, message)
        return
    context["deadline"] = message.text
    message = bot.send_message(
        message.from_user.id,
        f"Напишите техническое задание.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    bot.register_next_step_handler(
        message, lambda msg: get_order_details(bot, msg, context)
    )


def get_order_price(bot: TeleBot, message, context):
    category = context["category"]
    price = message.text
    price_exists = (
        session.query(Price)
        .filter(Price.price == price, Price.category == category.id)
        .scalar()
        is not None
    )
    if not price_exists:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        prices = session.query(Price).filter(Price.category == category.id).all()
        for price in prices:
            markup.add(types.KeyboardButton(price.price))
        message = bot.send_message(
            message.from_user.id,
            f"Вы выбрали неправильный бюджет. Отправьте еще раз.",
            reply_markup=markup,
        )
        bot.register_next_step_handler(
            message, lambda msg: get_order_price(bot, msg, context)
        )
        return
    context["price"] = price
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Сегодня (+ %100 от заказа)"))
    markup.add(types.KeyboardButton("Сутки (+ %50 от заказа)"))
    markup.add(types.KeyboardButton("2 дня (+ %15 от заказа)"))
    markup.add(types.KeyboardButton("2-4 дня"))
    message = bot.send_message(
        message.from_user.id,
        f"Вы берите сроки.",
        reply_markup=markup,
    )
    bot.register_next_step_handler(
        message, lambda msg: get_order_deadline(bot, msg, context)
    )


def handle_category_selection(bot, call):
    category_id = int(call.data.split("_")[-1])
    category = session.query(Category).filter(Category.id == category_id).first()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    prices = session.query(Price).filter(Price.category == category_id).all()
    for price in prices:
        markup.add(types.KeyboardButton(price.price))
    message = bot.send_message(
        call.from_user.id,
        f"Вы выбрали {category.name}.\nВыберите ваш бюджет.",
        reply_markup=markup,
    )
    context = {
        "category": category,
    }
    bot.register_next_step_handler(
        message, lambda msg: get_order_price(bot, msg, context)
    )
