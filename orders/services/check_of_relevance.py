from loguru import logger

from available_dates.models import AvailableDate
from orders.texts import error_messages
from services.models import Service


def data_is_relevance(data):
    """ Проверкаа актуальности данных """
    logger.info(data)
    if not _date_is_available(data['service_date_id']):
        return _raise_error(error_messages['date_is_not_valid'])
    else:
        if data['discount']:
            service = _service_data_is_valid(service_id=data['service_id'],
                                             price=data['service_price'],
                                             discount=data['discount'],
                                             discount_amount=data['discount_amount'])
        else:
            service = _service_data_is_valid(service_id=data['service_id'],
                                             price=data['service_price'])
        if not service['is_active']:
            return _raise_error(error_messages['service_is_not_active'])
        elif not service['price_is_valid']:
            return _raise_error(error_messages['price_is_changed'])

        if data['discount']:
            if not service['discount_is_valid']:
                return _raise_error(error_messages['discount_is_not_valid'])
            elif not service['discount_amount_is_valid']:
                return _raise_error(error_messages['discount_amount_is_not_valid'])
    return {"success": True}


def _raise_error(message):
    """ Возвращаем ошибку валидации """
    return {
        "success": False,
        "error_message": message
    }


def _date_is_available(date_id: int) -> bool:
    """ Проверяем свободна ли дата """
    date = AvailableDate.objects.get(pk=date_id)
    logger.info(date)
    logger.info(date.is_available)
    return date.is_available


def _service_data_is_valid(service_id: int, price, discount=None, discount_amount=None):
    """ Проверяем актуальны ли данные об услуге """
    service_data = {}
    service = Service.objects.get(pk=service_id)
    service_data['is_active'] = service.is_active
    logger.info(service.is_active)
    service_data['price_is_valid'] = service.price == price
    logger.info(service.price)
    if discount:
        service_data['discount_is_valid'] = service.discount
        logger.info(service.discount)
        service_data['discount_amount_is_valid'] = discount_amount == service.discount_amount
        logger.info(service.discount_amount)
    logger.info(service_data)
    return service_data
