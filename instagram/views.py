from loguru import logger
from loguru import logger
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from .models import Picture
from .serializers import PicturesListSerializer


class PicturesAdditionAPIview(GenericAPIView):
    """Добавление фотографии"""
    # permission_classes = (IsAdminUser,)
    serializer_class = PicturesListSerializer

    def post(self, request):
        logger.info(request.data)
        picture = PicturesListSerializer(data=request.data)
        logger.info(picture)
        try:
            picture_for_remove = Picture.objects.all().order_by('-id')[5:]
        except Exception as e:
            logger.error(e)

        else:
            [pic.delete() for pic in picture_for_remove]
            logger.info(picture_for_remove)
        if picture.is_valid():
            picture.save()
            logger.info(picture.data)

            return Response(data=picture.data, status=201)

        else:
            return Response(data={"success": False}, status=498)


class PicturesListAPIView(ListAPIView):
    """Список из 5-и последних добавленных фото"""
    # permission_classes = (IsAdminUser,)
    queryset = Picture.objects.filter(draft=False).order_by('-id')[:5]
    serializer_class = PicturesListSerializer

