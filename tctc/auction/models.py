from django.db import models


class Car(models.Model):
    """Машина"""
    release_date = models.IntegerField()
    mileage = models.IntegerField()
    first_price = models.DecimalField(max_digits=9, decimal_places=0)
    sell_price = models.DecimalField(max_digits=9, decimal_places=0)
    slug = models.SlugField()
    car_model = models.ForeignKey('CarModel', on_delete=models.CASCADE)
    engine = models.ForeignKey('Engine', on_delete=models.CASCADE)
    transmission = models.ForeignKey('Transmission', on_delete=models.SET_NULL, null=True)
    wheel = models.ForeignKey('Wheel', on_delete=models.SET_NULL, null=True)
    photo = models.ForeignKey('Images', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car_model.manufacturer.name}: должен возвратить марку авто текстом, {self.car_model.name}: должен возвратить модель авто текстом"

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Transmission(models.Model):
    """Коробка передач, тип и количество ступеней"""
    name = models.CharField(max_length=255)
    speed_cnt = models.IntegerField()


class Wheel(models.Model):
    """Привод автомобиля"""
    name = models.CharField(max_length=255)


class CarModel(models.Model):
    """Модель машины"""
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)


class Manufacturer(models.Model):
    """Производитель машины"""
    name = models.CharField(max_length=255)


class Engine(models.Model):
    """Объем и мощность двигателя"""
    volume = models.IntegerField()
    power = models.IntegerField()
    type = models.ForeignKey('EngineType', on_delete=models.CASCADE)


class EngineType(models.Model):
    """Тип двигателя"""
    name = models.CharField(max_length=255)


class Images(models.Model):
    """Много фотографий для одной машины"""
    image = models.ImageField(upload_to="carpics/%Y/%m/%d")
