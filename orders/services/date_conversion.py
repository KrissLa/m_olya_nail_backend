import pytz

WEEKDAYS = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def get_order_data(queryset):
    """ Преобразовываем данные о заказах """
    return [{"order_id": o['id'],
             "str_date": get_str_date(o)} for o in queryset]


def get_str_date(order):
    """ Преобразовываем дату в строку """
    return order["service_date__date"].astimezone(pytz.timezone("Europe/Minsk")).strftime("%d.%m.%Y %H:%M") + " " + \
           WEEKDAYS[order['service_date__date'].weekday()]
