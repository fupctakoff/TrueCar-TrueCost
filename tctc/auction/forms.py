from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from auction.models import Car, CarModel, Engine, Transmission, Wheel


# Шаги для FormWizard
class ManufacturerAndModelWizard(forms.ModelForm):
    """Шаг 1"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['manufacturer'].widget.attrs.update({'class': 'form-select'})
        self.fields['manufacturer'].empty_label = 'Выбрать производителя автомобиля'
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].empty_label = 'Выбрать тип двигателя'

    class Meta:
        model = Engine
        fields = ['type', 'volume', 'power']
        widgets = {
            'volume': forms.TextInput(attrs={'class': 'form-control', 'type': 'text',
                                             'placeholder': 'Введите объем двигателя через точку: 2.0'}),
            'power': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'})
        }


class TransmissionAndTransmissionTypeWizard(forms.ModelForm):
    """Шаг 3"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].empty_label = 'Выбрать тип коробки передач'

    class Meta:
        model = Transmission
        fields = ['type', 'speed_cnt']
        widgets = {
            'speed_cnt': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'})
        }


class WheelTypeWizard(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-select'})

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
        widgets = {
            'release_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'mileage': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'sell_price': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Ваше описание'}),
        }


class OurUserCreationForm(UserCreationForm):
    """Создание рядового пользователя"""
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OurUserAuthenticationForm(AuthenticationForm):
    """Форма для входа в аккаунт"""
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
