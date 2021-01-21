from django.urls import path

from . import views

urlpatterns = [
    path("", views.ServiceListAPIView.as_view()),
    path("<int:pk>/", views.ServiceRetrieveAPIView.as_view()),

]