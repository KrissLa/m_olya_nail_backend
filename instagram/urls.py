from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.PicturesAdditionAPIview.as_view()),
    path("pictures/", views.PicturesListAPIView.as_view()),
]