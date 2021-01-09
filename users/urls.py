from django.urls import path

from . import views

urlpatterns = [
    path("is_registered/<int:pk>/", views.IsUserRegisteredView.as_view()),
    path("get_id/<int:pk>/", views.UserIDView.as_view()),
    path("registration/", views.UserRegistrationAPIview.as_view()),

    path("can_be_invited/<int:pk>", views.UserCanBeInvitedView.as_view()),

]
