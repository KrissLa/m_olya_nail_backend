from loguru import logger

from olya_nail.settings import PERSONAL_CASHBACK_LEVEL, REFERRAL_CASHBACK_LEVEL, \
    REFERRAL_FIXED_BONUS, FIRST_BONUS
from orders.models import Order, Discount
from users.models import BonusTransaction


def confirm_order(order_id):
    """ Подтверждение завершения заказа """
    order = Order.objects.get(id=order_id)
    if order.status == "wait":
        order = order_change_status(order)
        bonus_points(order)
        personal_cashback(order.user)
        referral_bonus(order.user)
        order.user.save()
        order.save()
        return order
    elif order.status == "completed":
        return {"status": "already_completed"}
    else:
        return {"status": "canceled"}


def order_change_status(order):
    """ Переводим статус заказа в completed """
    order.status = "completed"
    return order


def bonus_points(order):
    """ Зачисление и списание бонусных баллов """
    bonus_points_write_off(order)
    bonus_points_enrollment(order)


def bonus_points_write_off(order):
    """ Списание бонусных баллов, потраченных при заказе """
    try:
        bonus = Discount.objects.get(order_id=order.id, type='points')
    except Discount.DoesNotExist:
        bonus = None
    logger.info(bonus)
    if bonus:
        logger.info(bonus.discount_amount)
        order.user.frozen_balance -= bonus.discount_amount
        bonus_transaction_write_off(order.user.id, bonus.discount_amount)


def bonus_transaction_write_off(user_id, amount):
    """ Создаем транзакцию 'списание' для истории операций с бонусными баллами """
    obj = BonusTransaction(user_id=user_id, type='write_off', amount=amount, comment="Оплата части заказа")
    obj.save()


def bonus_points_enrollment(order):
    """ Зачисление бонусных баллов """
    order.user.bonus_balance += order.bonus_points
    bonus_transaction_reward(order.user.id, order.bonus_points, "Успешное завершение заказа")


def bonus_transaction_reward(user_id, amount, comment):
    """ Создаем транзакцию 'зачисление' для истории операций с бонусными баллами """
    obj = BonusTransaction(user_id=user_id, type='reward', amount=amount, comment=comment)
    obj.save()


def personal_cashback(user):
    """ Проверяем уровень персонального кэшбэка и, если нужно, повышаем его"""
    actual_level = personal_cashback_check_level(user)
    if user.personal_cashback_level != actual_level:
        personal_cashback_level_up(user, actual_level)


def personal_cashback_check_level(user):
    """ Проверяем уровень персонального кэшбэка """
    completed_orders = Order.objects.filter(user_id=user.id, status='completed').count()
    user_level = user.personal_cashback_level
    return get_cashback_level(PERSONAL_CASHBACK_LEVEL, user_level, completed_orders)


def get_cashback_level(cashback_type, level, orders_count):
    """ Получаем уровень кэшбэка """
    while True:
        if level == 10:
            return level
        level_data = cashback_type[level]
        if bool(level_data['min_order_quantity'] <= orders_count < level_data['max_order_quantity']):
            if orders_count == level_data['max_order_quantity'] - 1:
                return level + 1
            return level
        level += 1



def personal_cashback_level_up(user, level):
    """ Повышаем уровень персональго кэшбэка """
    user.personal_cashback_level = level


def referral_bonus(user):
    """ Начисление бонусов пригласившему """
    if user.referer:
        if _is_first_order(user):
            _add_first_referer_bonus(user.referer)
        order_count = get_referral_order_count(user.referer.id)
        logger.info(order_count)
        referral_level = user.referer.referral_cashback_level
        actual_level = get_cashback_level(REFERRAL_CASHBACK_LEVEL, referral_level, order_count)
        if referral_level != actual_level:
            referral_level_up(user.referer, actual_level)
        if order_count % 10 == 0:
            add_referral_bonus(user.referer)
        user.referer.save()


def _is_first_order(user):
    """ Проверяем первый ли заказ пользователя"""
    orders_count = Order.objects.filter(user_id=user.id, status="completed").count()
    logger.info(orders_count)
    if orders_count == 0:
        return True
    return False


def _add_first_referer_bonus(referer):
    """ Начисляем бонус за первый заказ приглашенного пользователя"""
    referer.bonus_balance += REFERRAL_FIXED_BONUS
    bonus_transaction_reward(referer.id, FIRST_BONUS, "Бонус за первый заказ приглашенного пользователя")


def referral_level_up(referer, level):
    """ Повышаем реферальный уровень кэшбэка пригласившего """
    referer.referral_cashback_level = level


def get_referral_order_count(referer_id):
    """ Считаем общее количество заказов приглашенных пользователей """
    return Order.objects.filter(user__referer__id=referer_id, status='completed').count()


def add_referral_bonus(referer):
    """ Начисляем реферальный бонус за количество заказов приглашенных пользователей """
    referer.bonus_balance += REFERRAL_FIXED_BONUS
    bonus_transaction_reward(referer.id, REFERRAL_FIXED_BONUS, "Бонус за заказы приглашенных пользователей")
