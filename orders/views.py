from datetime import datetime, timedelta

import pytz
from loguru import logger
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, Discount, OrderRating
from orders.serializers import OrderDataSerializer, OrderDetailSerializer, OrderCancelSerializer, OrderRatingSerializer, \
    OrderRatingReviewSerializer, OrderRatingRatingViewedSerializer, \
    OrderRatingReviewViewedSerializer, OrderIsUserNotifiedSerializer
from orders.services.check_of_relevance import data_is_relevance
from orders.services.confirmation_order import confirm_order
from orders.services.date_conversion import get_order_data, WEEKDAYS
from orders.services.register import register_order


class OrderAPIView(APIView):
    """ Добавление заказа """

    # permission_classes = (IsAdminUser,)

    def post(self, request):
        logger.info(request.data)
        serializer = OrderDataSerializer(request.data)
        logger.info(serializer.data)
        check = data_is_relevance(serializer.data)
        logger.info(check)
        if not check['success']:
            return Response(data=check, status=status.HTTP_200_OK)
        order = register_order(serializer.data)

        return Response(data=order, status=status.HTTP_200_OK)


class OrderListMinView(APIView):
    """ Вывод списка заказов с минимальными данными"""

    def get(self, request):
        queryset = Order.objects.filter(status="wait").order_by("service_date__date").values("id", "service_date__date")
        data = get_order_data(queryset)
        logger.info(data)

        return Response(data=data)


class OrderDetailAPIView(RetrieveAPIView):
    """ Вывод информации о заказе """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.service_date.date = instance.service_date.date.astimezone(
            pytz.timezone("Europe/Minsk")).strftime("%d.%m.%Y %H:%M") + " " + \
                                     WEEKDAYS[instance.service_date.date.weekday()]
        serializer = self.get_serializer(instance)
        logger.info(serializer.data)
        return Response(serializer.data)


class OrderCancelAPIView(UpdateAPIView):
    """ Отмена заказа """
    queryset = Order.objects.all()
    serializer_class = OrderCancelSerializer

    def update(self, request, *args, **kwargs):
        discount = None
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        logger.info(instance.id)
        logger.info(instance)
        instance.service_date.is_available = True
        instance.service_date.save()
        logger.info(instance.service_date)
        try:
            discount = Discount.objects.get(order_id=instance.id,
                                            type='points')
            logger.info(discount.discount_amount)
            logger.info(discount)

        except Exception as err:
            logger.error(err)
        logger.info(discount)
        if discount:
            instance.user.frozen_balance -= discount.discount_amount
            instance.user.bonus_balance += discount.discount_amount
            instance.user.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class OrderConfirmAPIView(APIView):
    """ Подтверждение завершения заказа """

    def put(self, request, *args, **kwargs):
        logger.info(request)
        logger.info(kwargs['pk'])
        order = confirm_order(kwargs['pk'])
        try:
            ser = OrderDetailSerializer(order)
            data = ser.data
        except KeyError:
            data = order
        return Response(status=200, data=data)


class OrderRatingCreateAPIView(CreateAPIView):
    """ Добавление рейтинга к заказу """
    queryset = Order.objects.none()
    serializer_class = OrderRatingSerializer


class OrderRatingUpdateAPIView(UpdateAPIView):
    """ Обновление рейтинга (добавление отзыва) """
    queryset = OrderRating.objects.all()
    serializer_class = OrderRatingReviewSerializer
    lookup_field = 'order_id'


class OrderIsUserNotifiedAPIView(UpdateAPIView):
    """ Напоминае пользователю отправлено """
    queryset = Order.objects.all()
    serializer_class = OrderIsUserNotifiedSerializer
    lookup_field = 'id'


class OrderRatingRatingViewedAPIView(UpdateAPIView):
    """ Оценка просмотрена """
    queryset = OrderRating.objects.all()
    serializer_class = OrderRatingRatingViewedSerializer
    lookup_field = 'order_id'


class OrderRatingReviewViewedAPIView(UpdateAPIView):
    """ Отзыв просмотрен """
    queryset = OrderRating.objects.all()
    serializer_class = OrderRatingReviewViewedSerializer
    lookup_field = 'order_id'


class OrderRatingListAPIView(APIView):
    """ Вывод оценок к заказу """

    def get(self, request):
        queryset = OrderRating.objects.filter(rating_viewed=False)
        data = [
            {
                "order_id": q.order.id,
                "service_name": q.order.service_name,
                "service_date": q.order.service_date.date.astimezone(
                    pytz.timezone("Europe/Minsk")).strftime("%d.%m.%Y %H:%M") + " " + \
                                WEEKDAYS[q.order.service_date.date.weekday()],
                "rating": q.rating
            }
            for q in queryset
        ]
        logger.info(data)
        return Response(data=data)


class OrderReviewListAPIView(APIView):
    """ Вывод отзывов к заказу """

    def get(self, request):
        queryset = OrderRating.objects.filter(review_viewed=False)
        data = [
            {
                "order_id": q.order.id,
                "service_name": q.order.service_name,
                "service_date": q.order.service_date.date.astimezone(
                    pytz.timezone("Europe/Minsk")).strftime("%d.%m.%Y %H:%M") + " " + \
                                WEEKDAYS[q.order.service_date.date.weekday()],
                "review": q.review
            }
            for q in queryset
        ]
        logger.info(data)
        return Response(data=data)


class UserOrderListAPIView(ListAPIView):
    """ Список активных заказов пользователя """
    serializer_class = OrderDetailSerializer

    def get(self, request, telegram_id):
        logger.info(telegram_id)
        self.queryset = Order.objects.filter(user__telegram_id=telegram_id, status="wait").order_by("service_date__date")
        return self.list(request)


class OrderListForNotificationsAPIView(ListAPIView):
    """ Список заказов для отправки уведомлений пользователям """
    logger.info(datetime.now().date() + timedelta(days=1))
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.filter(is_user_notified=False,
                                    service_date__date__gt=datetime.now().date(),
                                    service_date__date__lt=datetime.now().date() + timedelta(days=2),
                                    status='wait')






    # class OrderListView(ListAPIView):
    #     """ Вывод списка заказов """
    #     filter_backends = (DjangoFilterBackend,)
    #     filterset_fields = ('user__telegram_id', 'status')
    #     queryset = Order.objects.all()
    #     serializer_class = OrderListSerializer
