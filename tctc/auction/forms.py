from django import forms
from django.core.exceptions import ValidationError

from auction.models import Car, CarModel, Engine, Transmission, Wheel


# в разработке
# class NameForm(forms.ModelForm):
#     CHOICES = []
#     manufacturers_queryset = Manufacturer.objects.all()
#     cnt = 0
#     for i in manufacturers_queryset:
#         CHOICES.append((cnt, i.name))
#         cnt += 1
#
#     manufacturer = forms.CharField(widget=forms.Select(choices=CHOICES))
#
#     class Meta:
#         model = Car
#         fields = ['manufacturer', 'car_model', 'release_date', 'mileage', 'sell_price']


# Шаги для FormWizard
class ManufacturerAndModelWizard(forms.ModelForm):
    """Шаг 1"""

    class Meta:
        model = CarModel
        fields = ['manufacturer', 'name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise ValidationError('Без пробелов')
        return name


class EngineAndEngineTypeWizard(forms.ModelForm):
    """Шаг 2"""

    class Meta:
        model = Engine
        fields = ['type', 'volume', 'power']


class TransmissionAndTransmissionTypeWizard(forms.ModelForm):
    """Шаг 3"""

    class Meta:
        model = Transmission
        fields = ['type', 'speed_cnt']


class WheelTypeWizard(forms.ModelForm):
    """Шаг 4"""
    w = Wheel.objects.all().select_related()
    name = forms.ChoiceField(choices=[(i, i) for i in w], label='Тип привода')

    class Meta:
        model = Wheel
        fields = ['name']


class CarWizard(forms.ModelForm):
    """Шаг 5"""

    class Meta:
        model = Car
        fields = ['release_date', 'mileage', 'sell_price', 'description']
