from django.db import models
from django.urls import reverse_lazy


class Car(models.Model):
    """Машина"""
    release_date = models.IntegerField(verbose_name='Год выпуска')
    mileage = models.IntegerField(verbose_name='Пробег, км.')
    first_price = models.DecimalField(max_digits=9, decimal_places=0, blank=True, default=10000,
                                      verbose_name='Стартовая цена, руб.')
    sell_price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Минимальная цена продажи, руб.')
    slug = models.SlugField()
    car_model = models.ForeignKey('CarModel', on_delete=models.CASCADE, verbose_name='Марка и модель')
    engine = models.ForeignKey('Engine', on_delete=models.CASCADE, verbose_name='Объем и мощность двигателя')
    transmission = models.ForeignKey('Transmission', on_delete=models.SET_NULL, null=True,
                                     verbose_name='Коробка передач')
    wheel = models.ForeignKey('Wheel', on_delete=models.SET_NULL, null=True, verbose_name='Привод')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(blank=True, default='Some description', verbose_name='Описание')

    def __str__(self):
        return f"{self.car_model.manufacturer.name} {self.car_model.name} {self.slug}"

    def get_absolute_url(self):
        return reverse_lazy('car_detail', kwargs={'slug': self.slug})

    # надо оптимизировать
    def get_first_photo(self):
        if self.images_set.all():
            return self.images_set.all().first().image.url
        return None

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобиль'
        ordering = ['-created_at', ]


class Transmission(models.Model):
    """Коробка передач, тип(по ключу) и количество ступеней"""
    speed_cnt = models.IntegerField()
    type = models.ForeignKey('TransmissionType', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type.name}, количество ступеней: {self.speed_cnt}"

    class Meta:
        verbose_name = 'Коробка передач'
        verbose_name_plural = 'Коробка передач'


class TransmissionType(models.Model):
    """Тип коробки передач"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип коробки передач'
        verbose_name_plural = 'Тип коробки передач'


class Wheel(models.Model):
    """Привод автомобиля"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Привод'
        verbose_name_plural = 'Привод'


class CarModel(models.Model):
    """Модель машины"""
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

    class Meta:
        verbose_name = 'Модель авто'
        verbose_name_plural = 'Модель авто'


class Manufacturer(models.Model):
    """Производитель машины"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель авто'
        verbose_name_plural = 'Производитель авто'


class Engine(models.Model):
    """Объем и мощность двигателя"""
    volume = models.FloatField()
    power = models.IntegerField()
    type = models.ForeignKey('EngineType', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type.name}, {self.volume} л., {self.power} л.с."

    class Meta:
        verbose_name = 'Двигатель'
        verbose_name_plural = 'Двигатель'


class EngineType(models.Model):
    """Тип двигателя"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип двигателя'
        verbose_name_plural = 'Тип двигателя'


class Images(models.Model):
    """Много фотографий для одной машины"""
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to="carpics/%Y/%m/%d")

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
