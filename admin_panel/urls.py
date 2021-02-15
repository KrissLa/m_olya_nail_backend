from django.urls import path

from . import views

urlpatterns = [
    path("", views.AdminPanelAPIView.as_view()),
]
