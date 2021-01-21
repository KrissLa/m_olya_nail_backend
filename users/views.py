from loguru import logger
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from olya_nail.settings import PERSONAL_CASHBACK_LEVEL, REFERAL_CASHBACK_LEVEL
from .models import BotUser, Referal
from .serializers import UserListSerializer, UserCanBeInvitedSerializer, UserIDSerializer, \
    UserBalanceSerializer
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
                             REFERAL_CASHBACK_LEVEL[levels.referral_cashback_level]['value']
        }
        logger.info(data)
        return Response(data=data, status=200)


class UserRegistrationAPIview(GenericAPIView):
    """Регистрация пользователя"""
    permission_classes = (IsAdminUser,)
    serializer_class = UserListSerializer

    def post(self, request):
        logger.info(request.data)
        user = UserListSerializer(data=request.data)
        if user.is_valid():
            user.save()
            logger.info(user.data)
            user_id = user.data['id']
            BotUserCashback(user_id=user_id,
                            personal_cashback_id=1,
                            referal_cashback_id=0).save()
            if "referer_id" in user.initial_data:
                data = add_referal(user, user_id)
            else:
                data = {
                    "bonus": 0,
                    "ref": None
                }
                logger.info("No referer")
            return Response(data=data, status=201)
        else:
            logger.info("Not valid")
            return Response(status=499)

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
