from datetime import datetime

from loguru import logger
from pytz import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Question
from .serializers import QuestionListSerializer
from .services.time_conversion import get_avg_time


class QuestionListCreateAPIView(ListCreateAPIView):
    """ Вывод списка вопросов и принятие пост запросов для создания вопроса"""
    # permission_classes = (IsAdminUser,)

    queryset = Question.objects.filter(is_answered=False)
    serializer_class = QuestionListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(serializer.data)
        avg_answer_time = get_avg_time()
        data = {
            "question_id": serializer.data['id'],
            "avg_answer_time": avg_answer_time,
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class AnswerAPIView(APIView):
    """ Добавление ответа на вопрос """

    # permission_classes = (IsAdminUser,)

    def post(self, request):
        logger.info(request.data)
        question = Question.objects.select_related('user').get(id=request.data["question_id"])   #filter(id=request.data["question_id"]).values()
        answer_time = datetime.now(timezone('UTC')) - question.created_at
        Question.objects.filter(id=request.data['question_id']).update(answer=request.data['answer'],
                                                                       is_answered=True,
                                                                       answered_at=datetime.now(),
                                                                       answer_time=answer_time.seconds)
        data = {
            "question_id": request.data["question_id"],
            "question": question.question,
            "answer": request.data["answer"],
            "telegram_id": question.user.telegram_id
        }
        return Response(data=data, status=status.HTTP_200_OK)


class QuestionListAPIView(APIView):
    """ Вывод отзывов к заказу """

    def get(self, request):
        queryset = Question.objects.filter(is_answered=False)
        data = [
            {
                "question_id": q.id,
                "user_name": q.user.name,
                "question": q.question,
                "user_tg_id": q.user.telegram_id
            }
            for q in queryset
        ]
        logger.info(data)
        return Response(data=data)
