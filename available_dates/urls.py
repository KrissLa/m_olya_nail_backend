from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.AvailableDateRetriveAPIView.as_view()),
    path("months/", views.AvailableDateListAPIView.as_view()),
    path("months/<int:month>/", views.AvailableDateDaysListAPIView.as_view()),
    path("months/<int:month>/<int:day>/", views.AvailableDateTimeListAPIView.as_view()),
]