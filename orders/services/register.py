from loguru import logger

from available_dates.models import AvailableDate
from orders.models import Order, Discount
from users.models import BotUser


def register_order(data):
    """ Регистрация заказа """
    _booking_date(data['service_date_id'])
    order_id = _create_order(data)
    logger.info(order_id)
    logger.info(data)
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


def _create_order(data):
    """ Создание заказа """
    user = BotUser.objects.get(telegram_id=data['telegram_id'])
    order = Order(user_id=user.id,
                  service_date_id=data['service_date_id'],
                  service_name=data['service_name'],
                  service_price=data['service_price'],
                  total_price=data['total_price'],
                  bonus_points=data['bonus_points']
                  )
    order.save()
    return order.id


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
