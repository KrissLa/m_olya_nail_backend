from loguru import logger
from ..models import BotUser

from olya_nail.settings import FREE_BONUS, REFERRAL_BONUS, FREE_CODE


def add_referal(user, user_id):
    """Добавляем связи между пригласившим и приглашенным"""
    user_telegram_id = user.initial_data['telegram_id']
    referer_tg_id = user.initial_data['referer_id']
    if _is_free_code(referer_tg_id):
        logger.info("Нашел бонус код")
        _add_bonus(FREE_BONUS, user_id)
        return {
            "bonus": FREE_BONUS,
            "ref": None
        }
    try:
        logger.info("Вошел в try")
        if _is_valid_referer(referer_tg_id, user_telegram_id):
            logger.info("Прошел проверку на валидность")
            referer = BotUser.objects.get(telegram_id=referer_tg_id)
            _add_referer(referer.id, user_id)
            _add_bonus(REFERRAL_BONUS, user_id)
            logger.info("ref and balance update")
            return {
                "bonus": REFERRAL_BONUS,
                "ref": referer.name
            }

        else:
            logger.info("ref NOT valid")
            return {
                "bonus": 0,
                "ref": None
            }
    except ValueError:
        logger.error("КОД не валидный")
        return {
            "bonus": 0,
            "ref": None
        }


def _add_referer(referer_id, user_id):
    """Добавляем реферальную связь в таблицу"""
    Referral(referer_id=referer_id,
             referral_id=user_id).save()


def _add_bonus(bonus, user_id):
    """Начисляем бонус"""
    new_user = BotUser.objects.get(id=user_id)
    new_user.bonus_balance = bonus
    new_user.can_be_invited = False
    new_user.save()


def _is_valid_referer(referer_id: int, user_id: int) -> bool:
    """Проверяем допустимы ли referer_id"""
    if referer_id == user_id:
        return False
    try:
        referer = BotUser.objects.get(telegram_id=referer_id)
    except BotUser.DoesNotExist:
        referer = None
    if referer:
        return True
    return False


def _is_free_code(referer_code) -> bool:
    """Проверяем стандартную пригласительную ссылку"""
    if referer_code == FREE_CODE:
        return True
    return False
