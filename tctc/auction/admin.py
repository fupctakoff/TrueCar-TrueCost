from django.contrib import admin
from .models import Car, Transmission, TransmissionType, Wheel, CarModel, Manufacturer, Engine, EngineType, Images


class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'created_at']


admin.site.register(Car, CarAdmin)
admin.site.register(Transmission)
admin.site.register(TransmissionType)
admin.site.register(Wheel)
admin.site.register(CarModel)
admin.site.register(Manufacturer)
admin.site.register(Engine)
admin.site.register(EngineType)
admin.site.register(Images)
