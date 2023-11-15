from django.db import models
from pick.func import get_path_upload_photos

# модель туриста не на базе встроенной модели User, тк по техзаданию не требуется регистрация
class User(models.Model):
    email = models.EmailField()
    fam = models.TextField(max_length=255,verbose_name='Фамилия')
    name = models.TextField(max_length=255, verbose_name='Имя')
    otc = models.TextField(max_length=255, verbose_name='Отчество')
    phone = models.TextField(max_length=255, verbose_name='Контактный телефон')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['email'], name="user_unique")]
    def __str__(self):
        return f"{self.fam} {self.name} {self.otc}"

class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def __str__(self):
        return f"широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}"

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"

class Level(models.Model):
    winter = models.TextField(verbose_name='Зима', null=True, blank=True)
    summer = models.TextField(verbose_name='Лето', null=True, blank=True)
    autumn = models.TextField(verbose_name='Осень', null=True, blank=True)
    spring = models.TextField(verbose_name='Весна', null=True, blank=True)

    def __str__(self):
        return f"зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}"

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"

class Pereval(models.Model):
    STATUS_CHOICES = [
        ("new", "новый"),
        ("pending", "в работе"),
        ("accepted", "принят"),
        ("rejected", "отклонен"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES)
    beauty_title = models.TextField(blank=True,verbose_name='Основное название вершины', null=True)
    title = models.TextField(blank=True, null=True, verbose_name='Название вершины')
    other_titles = models.TextField(blank=True, null=True,verbose_name='Другое название' )
    connect = models.TextField(blank=True,verbose_name='Связывает', null=True)
    add_time = models.TimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.pk}: {self.beauty_title}"

    class Meta:
        verbose_name = "pereval_added"
        verbose_name_plural = "Перевалы"

    def create_pereval(self, pereval_data):
        # Создание новой записи перевала
        pereval_object = self.create(**pereval_data)
        # Установка значения поля status в "new"
        pereval_object.status = "new"
        pereval_object.save()
        return pereval_object

class Image(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    data = models.ImageField(max_length=2000, upload_to=get_path_upload_photos, verbose_name='Изображение', null=True, blank=True)
    title = models.TextField(max_length=255, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}: {self.title}"

    class Meta:
        verbose_name = "Изображения"






