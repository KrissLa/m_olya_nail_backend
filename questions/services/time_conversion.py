from loguru import logger

from ..models import Question


def get_avg_time():
    """ Получаем среднее время ответа """
    answer_time = Question.objects.filter(answer_time__gt=0).only('answer_time')
    list_with_time = [t.answer_time for t in answer_time]
    try:
        avg_time = int(sum(list_with_time) / len(list_with_time))
    except ZeroDivisionError:
        return None
    return get_str_time(avg_time)

def get_str_time(seconds: int) -> str:
    """ Преобразование количества секунд в строку"""
    if seconds < 60:
        return _get_str_seconds(seconds)
    elif seconds < 3600:
        return _get_str_minutes(seconds)
    elif seconds < 86400:
        return _get_str_hours(seconds)
    else:
        return _get_str_days(seconds)


def _get_str_seconds(seconds: int) -> str:
    """ Преобразование количества секунд в строку """
    last_digit = int(str(seconds)[-1])
    logger.info(last_digit)
    if seconds in [11, 12, 13, 14]:
        sec = "секунд"
    elif last_digit == 1:
        sec = "секунда"
    elif last_digit in [2, 3, 4]:
        sec = "секунды"
    else:
        sec = "секунд"
    return f"{seconds} {sec}"


def _get_str_minutes(seconds: int) -> str:
    """ Преобразование количества секунд в строку с минутами"""
    minutes = seconds // 60
    last_digit = int(str(minutes)[-1])
    logger.info(last_digit)
    if minutes in [11, 12, 13, 14]:
        min = "минут"
    elif last_digit == 1:
        min = "минута"
    elif last_digit in [2, 3, 4]:
        min = "минуты"
    else:
        min = "минут"
    return f"{minutes} {min}"


def _get_str_hours(seconds: int) -> str:
    """ Преобразование количества секунд в строку с часами и минутами"""
    hours = seconds // 3600
    seconds_for_minutes = seconds % 3600
    last_digit = int(str(hours)[-1])
    logger.info(last_digit)
    if hours in [11, 12, 13, 14]:
        str_hour = "часов"
    elif last_digit in [2, 3, 4]:
        str_hour = "часа"
    elif last_digit == 1:
        str_hour = "час"
    else:
        str_hour = "часов"
    return f"{hours} {str_hour} {_get_str_minutes(seconds_for_minutes)}"


def _get_str_days(seconds: int) -> str:
    """ Преобразование количества секунд в строку с днями, часами и минутами"""
    days = seconds // 86400
    sec_for_hours = seconds % 86400
    sec_for_minutes = (seconds % 86400) % 3600
    last_digit = int(str(days)[-1])
    logger.info(last_digit)
    if days in [11, 12, 13, 14]:
        str_days = "дней"
    elif last_digit == 1:
        str_days = "день"
    elif last_digit in [2, 3, 4]:
        str_days = "дня"
    else:
        str_days = "дней"
    return f"{days} {str_days} {_get_str_hours(sec_for_hours)}"
