from django.http import JsonResponse
from .serializers import *
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .models import Pereval


# от ModelViewSet все виды запросов
class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer
class CoordsViewSet(viewsets.ModelViewSet):
        queryset = Coords.objects.all()
        serializer_class = CoordsSerializer

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = LevelSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    # создание перевала
    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)

        """Результаты метода: JSON"""
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных',
                'id': None,
            })
    # редактирование объекта перевала, если статус все еще new и данные о самом пользователе не меняются.
    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == 'new':
            serializer = PerevalSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись успешно изменена'
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f"Не удалось обновить запись, так как сведения уже у модератора и имеют статус: {pereval.get_status_display()}"
            })

# список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер.
class EmailAPIView(generics.ListAPIView):
    serializer_class = PerevalSerializer
    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Pereval.objects.filter(user__email=email):
            data = PerevalSerializer(Pereval.objects.filter(user__email=email), many=True).data
            api_status = status.HTTP_200_OK
        else:
            data = {
                'message': f'Не существует пользователя с таким email - {email}'
            }
            api_status = 404
        return JsonResponse(data, status=api_status, safe=False)