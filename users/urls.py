from django.urls import path

from . import views

urlpatterns = [
    path("is_registered/<int:pk>/", views.IsUserRegisteredView.as_view()),
    path("get_id/<int:pk>/", views.UserIDView.as_view()),
    path("bonus/<int:telegram_id>/", views.UserBonusAPIView.as_view()),
    path("bonus_transactions/<int:telegram_id>/", views.UserBonusTransactionListAPIView.as_view()),
    path("get_bonus_balance/<int:pk>/", views.UserBonusBalanceView.as_view()),
    path("get_cashback/<int:telegram_id>/", views.UserCashbackView.as_view()),
    path("registration/", views.UserRegistrationAPIView.as_view()),
    path("profile/<int:telegram_id>/", views.UserProfileAPIView.as_view()),

]
