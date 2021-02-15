from datetime import timedelta, date, datetime

from loguru import logger
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import pytz
from .models import AvailableDate
from .serializers import AvailableDateListSerializer


class AvailableDateListAPIView(APIView):
    """Список доступных месяцев"""

    # permission_classes = (IsAdminUser,)

    def get(self, request):
        logger.info(timezone.now())
        logger.info(datetime.now().date() + timedelta(days=1))
        queryset = AvailableDate.objects.filter(is_available=True,
                                                date__gt=datetime.now().date() + timedelta(days=1)).datetimes('date',
                                                                                                              'month')
        logger.info(queryset)
        logger.info(queryset.values())
        months = [d.month for d in queryset]
        return Response(data={'months': months})


class AvailableDateDaysListAPIView(APIView):
    """ Список доступных дней в месяце """

    # permission_classes = (IsAdminUser,)
    def get(self, request, month):
        queryset = AvailableDate.objects.filter(is_available=True,
                                                date__gt=datetime.now().date() + timedelta(days=1),
                                                date__month=month).datetimes('date', 'day')
        logger.info(queryset)
        logger.info(queryset.values())
        days = [{"day": d.day, "day_of_week": d.weekday()} for d in queryset]
        return Response(data={'days': days})


class AvailableDateTimeListAPIView(APIView):
    """ Список доступных окошек в день """

    # permission_classes = (IsAdminUser,)
    def get(self, request, month, day):
        queryset = AvailableDate.objects.filter(is_available=True,
                                                date__gt=timezone.now(),
                                                date__month=month,
                                                date__day=day).order_by("date")
        dates = [{'available_date_id': d['id'],
                  'date': d['date'].astimezone(pytz.timezone("Europe/Minsk")).strftime("%d.%m.%Y %H-%M")} for d in
                 queryset.values()]
        logger.info(dates)

        return Response(data=dates)


class AvailableDateRetriveAPIView(RetrieveAPIView):
    """ Получаем информацию о дате """
    # permission_classes = (IsAdminUser,)
    queryset = AvailableDate.objects.filter(is_available=True,
                                            date__gt=timezone.now())
    serializer_class = AvailableDateListSerializer
