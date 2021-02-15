from rest_framework import serializers

from available_dates.models import AvailableDate
from available_dates.serializers import AvailableDateListSerializer
from orders.models import Order, Discount, OrderRating
from users.models import BotUser


class OrderDataSerializer(serializers.Serializer):
    """ Сериализация данных о заказе """
    telegram_id = serializers.IntegerField()
    service_date_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=4, decimal_places=2)
    service_price = serializers.IntegerField()
    service_time = serializers.CharField(max_length=25)
    discount = serializers.BooleanField()
    discount_amount = serializers.IntegerField()
    discount_amount_BYN = serializers.DecimalField(max_digits=4, decimal_places=2)
    bonus_discount = serializers.BooleanField()
    bonus_discount_amount = serializers.IntegerField()
    bonus_discount_amount_BYN = serializers.DecimalField(max_digits=4, decimal_places=2)
    bonus_points = serializers.IntegerField()
    service_name = serializers.CharField(max_length=255)


class DiscountSerializer(serializers.ModelSerializer):
    """ Сериализация скидок """
    class Meta:
        model = Discount
        fields = "__all__"


class BotUserSerializer(serializers.ModelSerializer):
    """ Сериализация пользователя"""
    class Meta:
        model = BotUser
        fields = ("id", "telegram_id", "name", "username", "phone_number", )


class OrderDetailSerializer(serializers.ModelSerializer):
    """ Сериализация заказов """
    discounts = DiscountSerializer(read_only=True, many=True)
    service_date = AvailableDateListSerializer(read_only=True)
    user = BotUserSerializer(read_only=True)
    class Meta:
        model = Order
        # fields = ("user", "service_date", "date", "service_name", "service_price", "total_price", "bonus_points",
        #           "status", "is_user_notified", "discounts")
        fields = "__all__"


class OrderListMinSerializer(serializers.ModelSerializer):
    """ Сериализация заказов """
    service_date = AvailableDateListSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ("id", "service_date")


class OrderCancelSerializer(serializers.ModelSerializer):
    """ Сериализация для отмены заказа """
    service_date = AvailableDateListSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'status', 'reason_for_reject', 'service_date')


class OrderRatingSerializer(serializers.ModelSerializer):
    """ Сериализация отзывов к заказу """
    class Meta:
        model = OrderRating
        fields = "__all__"


class OrderRatingReviewSerializer(serializers.ModelSerializer):
    """ Сериализация отзывов к заказу """
    class Meta:
        model = OrderRating
        fields = ('review', 'review_viewed')


class OrderIsUserNotifiedSerializer(serializers.ModelSerializer):
    """ Поле просмотра оценки """
    class Meta:
        model = Order
        fields = ('is_user_notified',)


class OrderRatingRatingViewedSerializer(serializers.ModelSerializer):
    """ Поле просмотра оценки """
    class Meta:
        model = OrderRating
        fields = ('rating_viewed',)


class OrderRatingReviewViewedSerializer(serializers.ModelSerializer):
    """ Поле просмотра отзыва """
    class Meta:
        model = OrderRating
        fields = ('review_viewed',)
