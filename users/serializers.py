from rest_framework import serializers
from .models import BotUser


class UserListSerializer(serializers.ModelSerializer):
    """ Список пользователей """

    class Meta:
        model = BotUser
        fields = "__all__"


class UserIDSerializer(serializers.ModelSerializer):
    """ ID пользователя """

    class Meta:
        model = BotUser
        fields = ("id",)


class UserCanBeInvitedSerializer(serializers.ModelSerializer):
    """ Проверяем может ли пользователь быть приглашен """

    class Meta:
        model = BotUser
        fields = ("can_be_invited",)

class UserBalanceSerializer(serializers.ModelSerializer):
    """ Получаем бонусный баланс пользователя """

    class Meta:
        model = BotUser
        fields = ("bonus_balance",)


# class PersonalCashbackSerializer(serializers.ModelSerializer):
#     """ Сериализация уровней кэшбэка """
#
#     class Meta:
#         model = PersonalCashback
#         fields = ("level",)


# class ReferalCashbackSerializer(serializers.ModelSerializer):
#     """ Сериализация уровней кэшбэка """
#
#     class Meta:
#         model = ReferalCashback
#         fields = ("level",)


# class BotUserCashbackSerializer(serializers.ModelSerializer):
#     """ Сериализатор для кэшбека пользователя """
#     referal_cashback_id = PersonalCashbackSerializer(read_only=True)
#     personal_cashback_id = ReferalCashbackSerializer(read_only=True)
#     user_id = UserListSerializer(read_only=True)
#
#     class Meta:
#         model = BotUserCashback
#         fields = ("user_id", "personal_cashback_id", "referal_cashback_id")
