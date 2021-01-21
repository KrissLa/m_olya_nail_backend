from django.shortcuts import render

# Create your views here.
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.serializers import OrderDataSerializer
from orders.services.check_of_relevance import data_is_relevance
from orders.services.register import register_order


class OrderAPIView(APIView):
    """ Добавление заказа """
    {
        "telegram_id": 557615633,
        "service_date_id": 10,
        "service_id": 2,
        "total_price": 20,
        "discount": "true",
        "discount_amount": 10,
        "discount_amount_BYN": 2.5,
        "bonus_discount": "true",
        "bonus_discount_amount": 500,
        "bonus_discount_amount_BYN": 0.5,
        "bonus_points": 200,
        "service_name": "Маник",
        "total_price": 22,
        "service_price": 25
    }

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
