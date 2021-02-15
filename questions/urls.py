from django.urls import path

from . import views

urlpatterns = [
    path("", views.QuestionListCreateAPIView.as_view()),
    path("answer/", views.AnswerAPIView.as_view()),
    path("list/", views.QuestionListAPIView.as_view()),

]