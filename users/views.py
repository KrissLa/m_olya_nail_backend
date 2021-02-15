from loguru import logger
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from olya_nail.settings import PERSONAL_CASHBACK_LEVEL, REFERRAL_CASHBACK_LEVEL, REFERRAL_BONUS, FREE_BONUS
from orders.models import Order
from orders.services.confirmation_order import bonus_transaction_reward
from .models import BotUser, BonusTransaction
from .serializers import UserListSerializer, UserCanBeInvitedSerializer, UserIDSerializer, \
    UserBalanceSerializer, UserDetailSerializer, UserDataSerializer, UserProfileSerializer, \
    BonusTransactionListSerializer
from .servisec.registration import add_referal


class UserIDView(APIView):
    """ Получаем user_id по телеграм id"""

    # permission_classes = (IsAdminUser,)
    def get(self, request, pk):
        try:
            user = BotUser.objects.get(telegram_id=pk)
        except Exception as e:
            user = None
        if user:
            serializer = UserIDSerializer(user)
            return Response(serializer.data)
        return Response(data={"user_id": 0}, status=407)


class IsUserRegisteredView(APIView):
    """ Информация о том, зарегистрирован ли пользователь"""

    # permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        logger.info(request.data)
        try:
            user = BotUser.objects.get(telegram_id=pk)
        except Exception as e:
            logger.error(e)
            user = False
        logger.info(user)
        if user:
            user = True
        return Response(user)


class UserCanBeInvitedView(APIView):
    """ Информация о том, может ли пользователь быть приглашен """
    permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        can_be_invited = BotUser.objects.get(telegram_id=pk)
        serializer = UserCanBeInvitedSerializer(can_be_invited)
        return Response(serializer.data)


class UserBonusBalanceView(APIView):
    """ Информация о бонусном балансе пользователя """

    # permission_classes = (IsAdminUser,)

    def get(self, request, pk):
        user = BotUser.objects.get(telegram_id=pk)
        serializer = UserBalanceSerializer(user)
        return Response(serializer.data)


class UserCashbackView(APIView):
    """ Информация о кэшбэке пользователя """

    # permission_classes = (IsAdminUser,)

    def get(self, request, telegram_id):
        levels = BotUser.objects.get(telegram_id=telegram_id)
        data = {
            'user_cashback': PERSONAL_CASHBACK_LEVEL[levels.personal_cashback_level]['value'] +
                             REFERRAL_CASHBACK_LEVEL[levels.referral_cashback_level]['value']
        }
        logger.info(data)
        return Response(data=data, status=200)


class UserBonusAPIView(APIView):
    """ Вывод информации о бонусах пользователя """

    def get(self, request, telegram_id):
        user = BotUser.objects.get(telegram_id=telegram_id)
        # logger.info(**user)
        user_orders = Order.objects.filter(user_id=user.id, status="completed").count()
        logger.info(user_orders)
        user_ref_orders = Order.objects.filter(user__referer_id=user.id, status="completed").count()
        logger.info(user_ref_orders)
        if user.personal_cashback_level == 10:
            p_left = "Достигнут максимальный уровень"
        else:
            p_left = PERSONAL_CASHBACK_LEVEL[user.personal_cashback_level]['max_order_quantity'] - user_orders
        if user.referral_cashback_level == 10:
            r_left = "Достигнут максимальный уровень"
        else:
            r_left = REFERRAL_CASHBACK_LEVEL[user.referral_cashback_level]['max_order_quantity'] - user_ref_orders
        data = {
            "personal_lvl": user.personal_cashback_level,
            "personal_value": PERSONAL_CASHBACK_LEVEL[user.personal_cashback_level]['value'],
            "personal_orders_left": p_left,
            "referral_lvl": user.referral_cashback_level,
            "referral_value": REFERRAL_CASHBACK_LEVEL[user.referral_cashback_level]['value'],
            "referral_orders_left": r_left,
            "bonus_balance": user.bonus_balance,
            "frozen_balance": user.frozen_balance,
        }
        logger.info(data)
        return Response(data=data, status=200)


class UserRegistrationAPIView(GenericAPIView):
    """
    Регистрация пользователя
    """
    serializer_class = UserDetailSerializer

    def post(self, request):
        serializer = UserDataSerializer(request.data)
        register_data = dict(serializer.data)
        if register_data['referer']:
            try:
                ref = BotUser.objects.get(telegram_id=register_data['referer'])
            except BotUser.DoesNotExist:
                register_data.pop('referer')
                register_data['bonus_balance'] = FREE_BONUS
            else:
                register_data['referer'] = ref.id
                register_data['bonus_balance'] = REFERRAL_BONUS
        else:
            register_data['bonus_balance'] = FREE_BONUS
        register_data['personal_cashback_level'] = 1
        register_data['referral_cashback_level'] = 0
        register_data['frozen_balance'] = 0
        user = UserDetailSerializer(data=register_data)
        if user.is_valid(raise_exception=True):
            new_user = user.save()
            bonus_transaction_reward(user_id=new_user.id, amount=new_user.bonus_balance, comment="Бонус за регистрацию")
            data = dict(user.data)
            if data['referer']:
                data['ref_name'] = ref.name
            return Response(status=201, data=data)
        return Response(status=200, data={'success': False})


class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Информация о профиле пользователя
    """
    serializer_class = UserProfileSerializer
    queryset = BotUser.objects.all()
    lookup_field = "telegram_id"


class UserBonusTransactionListAPIView(ListAPIView):
    """ Список активных заказов пользователя """
    serializer_class = BonusTransactionListSerializer

    def get(self, request, telegram_id):
        logger.info(telegram_id)
        self.queryset = BonusTransaction.objects.filter(user__telegram_id=telegram_id).order_by("-id")[:10]
        return self.list(request)






# class UserRegistrationAPIview(GenericAPIView):
#     """Регистрация пользователя"""
#     permission_classes = (IsAdminUser,)
#     serializer_class = UserListSerializer
#
#     def post(self, request):
#         logger.info(request.data)
#         user = UserListSerializer(data=request.data)
#         if user.is_valid():
#             user.save()
#             logger.info(user.data)
#             user_id = user.data['id']
#             BotUserCashback(user_id=user_id,
#                             personal_cashback_id=1,
#                             referal_cashback_id=0).save()
#             if "referer_id" in user.initial_data:
#                 data = add_referal(user, user_id)
#             else:
#                 data = {
#                     "bonus": 0,
#                     "ref": None
#                 }
#                 logger.info("No referer")
#             return Response(data=data, status=201)
#         else:
#             logger.info("Not valid")
#             return Response(status=499)

# class UserListView(APIView):
#     """ Список пользователей """
#
#     # permission_classes = (IsAdminUser,)
#
#
#     def get(self, request):
#         users = BotUser.objects.all()
#         serializer = UserListSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         user = UserListSerializer(data=request.data)
#         if user.is_valid():
#             user.save()
#             return Response(status=201, data="Пользователь успешно добавлен")
#         return Response(status=404, data="Не удалось добавить пользователя")
#
#
# # class UserListView(APIView):
# #     """ Список пользователей """
# #
# #     # permission_classes = (IsAuthenticated,)
# #     def get_queryset(self):
# #         return BotUser.objects.all()
# #
# #     def get(self, request):
# #         users = BotUser.objects.all()
# #         serializer = UserListSerializer(users, many=True)
# #         return Response(serializer.data)
# #
# #     def post(self, request):
# #         user = UserListSerializer(data=request.data)
# #         if user.is_valid():
# #             user.save()
# #             return Response(status=201, data="Пользователь успешно добавлен")
# #         return Response(status=404, data="Не удалось добавить пользователя")
#
#
# class UserDetailView(APIView):
#     """ Пользователь """
#
#     def get_queryset(self):
#         return BotUser.objects.all()
#
#     def get(self, request, pk):
#         print(request)
#         user = BotUser.objects.get(id=pk)
#         serializer = UserListSerializer(user)
#         return Response(serializer.data)
