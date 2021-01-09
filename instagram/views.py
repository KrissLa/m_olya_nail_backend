from django.shortcuts import render
from loguru import logger
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PicturesListSerializer
from .models import Picture


class PicturesAdditionAPIview(GenericAPIView):
    """Добавление фотографии"""
    # permission_classes = (IsAdminUser,)
    serializer_class = PicturesListSerializer

    def post(self, request):
        logger.info(request.data)
        picture = PicturesListSerializer(data=request.data)
        logger.info(picture)
        if picture.is_valid():
            picture.save()
            logger.info(picture.data)
            return Response(data=picture.data, status=201)
        else:
            return Response(data={"success": False}, status=498)


class PicturesListAPIView(ListAPIView):
    """Список из 5-и последних добавленных фото"""
    queryset = Picture.objects.filter(draft=False).order_by('-id')[:5]
    serializer_class = PicturesListSerializer

