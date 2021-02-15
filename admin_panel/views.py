from loguru import logger
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Order, OrderRating
from questions.models import Question


class AdminPanelAPIView(APIView):
    """ Вывод количества новых событий в админку бота """
    def get(self, request):
        orders = Order.objects.filter(status="wait").count()
        ratings = OrderRating.objects.filter(rating_viewed=False).count()
        reviews = OrderRating.objects.filter(review_viewed=False).count()
        questions = Question.objects.filter(is_answered=False).count()
        data = {
            "orders_number": orders,
            "ratings_number": ratings,
            "reviews_number": reviews,
            "questions_number": questions,
        }
        return Response(status=200, data=data)