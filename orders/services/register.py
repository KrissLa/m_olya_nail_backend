from datetime import datetime

import pytz
from dateutil.parser import parse
from loguru import logger

from available_dates.models import AvailableDate
from orders.models import Order, Discount
from users.models import BotUser


def register_order(data):
    """ Регистрация заказа """
    order_date = _booking_date(data['service_date_id'])
    order_id = _create_order(data, order_date)
    _add_discounts(data, order_id)
    return {
        "success": True,
        "order_id": order_id,
    }


def _booking_date(date_id):
    """ Бронирование даты """
    date = AvailableDate.objects.get(id=date_id)
    date.is_available = False
    date.save()
    logger.info(date.date)
    return date.date


def _create_order(data, order_date):
    """ Создание заказа """
    logger.info(data)
    user = BotUser.objects.get(telegram_id=data['telegram_id'])
    order = Order(user_id=user.id,
                  service_date_id=data['service_date_id'],
                  service_name=data['service_name'],
                  service_price=data['service_price'],
                  service_time=data['service_time'],
                  total_price=data['total_price'],
                  bonus_points=data['bonus_points'],
                  is_user_notified=_check_date_for_notification(order_date)
                  )
    order.save()
    logger.info(order.is_user_notified)
    return order.id


def _check_date_for_notification(date):
    """
    Проверяем нужно ли будет отправить оповещение пользователю
    """
    logger.info(date)
    logger.info(date.astimezone(pytz.timezone("Europe/Minsk")))
    logger.info(type(date))
    logger.info(isinstance(date, datetime))
    delta = date.astimezone(pytz.timezone("Europe/Minsk")) - datetime.now().astimezone(pytz.timezone("Europe/Minsk"))
    logger.info(delta)
    logger.info(delta.days)
    if delta.days > 1:
        return False
    return True


def _add_discounts(data, order_id):
    """ Добавление скидок """
    logger.info(data)
    if data['discount']:
        discount = Discount(order_id=order_id,
                            type="percent",
                            discount_amount=data['discount_amount'],
                            discount_amount_BYN=data['discount_amount_BYN'])
        discount.save()
    if data['bonus_discount']:
        bonus_discount = Discount(order_id=order_id,
                                  type="points",
                                  discount_amount=data['bonus_discount_amount'],
                                  discount_amount_BYN=data['bonus_discount_amount_BYN'])
        bonus_discount.save()
        user = BotUser.objects.get(telegram_id=int(data['telegram_id']))
        user.bonus_balance -= data['bonus_discount_amount']
        user.frozen_balance += data['bonus_discount_amount']
        user.save()
