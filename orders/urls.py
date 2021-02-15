from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.OrderAPIView.as_view()),
    path("min_list/", views.OrderListMinView.as_view()),
    path("<int:pk>/", views.OrderDetailAPIView.as_view()),
    path("user/<int:telegram_id>/", views.UserOrderListAPIView.as_view()),
    path("cancel/<int:pk>/", views.OrderCancelAPIView.as_view()),
    path("confirm/<int:pk>/", views.OrderConfirmAPIView.as_view()),
    path("rating/add/", views.OrderRatingCreateAPIView.as_view()),
    path("rating/list/", views.OrderRatingListAPIView.as_view()),
    path("reviews/list/", views.OrderReviewListAPIView.as_view()),
    path("rating/update/<int:order_id>/", views.OrderRatingUpdateAPIView.as_view()),
    path("rating/rating_viewed/<int:order_id>/", views.OrderRatingRatingViewedAPIView.as_view()),
    path("rating/review_viewed/<int:order_id>/", views.OrderRatingReviewViewedAPIView.as_view()),
    path("notifications/", views.OrderListForNotificationsAPIView.as_view()),
    path("notification_was_sent/<int:id>/", views.OrderIsUserNotifiedAPIView.as_view()),
]