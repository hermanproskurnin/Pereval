from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import User, Coords, Level, Pereval, Image

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fam', 'name', 'otc', 'phone')
        verbose_name = 'Турист'

    def save(self, **kwargs):
        self.is_valid()
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            return User.objects.create(
                email=self.validated_data.get('email'),
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
            )
class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')
        verbose_name = 'Координаты'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'summer', 'autumn', 'spring')
        verbose_name = 'Уровень сложности'


class ImageSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Image
        fields = ('data', 'title')
        verbose_name = 'Фото'


# основной сериалайзер с вложенными данными
class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = (
            'id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level', 'images', 'status')
        read_only_fields = ['status']

    # Сохранение данных о перевале, полученных от пользователя
    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        # проверка уникальности пользователя
        pick_user = User.objects.filter(email=user['email'])
        if pick_user.exists():
            user_serializer = UserSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        else:
            user = User.objects.create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        pereval = Pereval.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')

        for image in images:
            data = image.pop('data')
            title = image.pop('title')
            Image.objects.create(data=data, pereval=pereval, title=title)

        return pereval

    # выполняет ТЗ о невозможности изменять данные пользователя при редактировании данных о перевале
    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            validating_user_fields = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(validating_user_fields):
                raise serializers.ValidationError({'Данные пользователя не могут быть изменены'})
        return data


