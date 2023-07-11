import os

from django.conf import settings
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from formtools.wizard.views import SessionWizardView

from .forms import ManufacturerAndModelWizard, EngineAndEngineTypeWizard, \
    TransmissionAndTransmissionTypeWizard, WheelTypeWizard, CarWizard, OurUserCreationForm, OurUserAuthenticationForm
from .models import Car, Images, CarModel, Engine, Transmission, Wheel
from random import randint


# class ListOfAuctions(ListView):
#     """Список всех проданных автомобилей"""
#     model = Car
#     template_name = 'auction/main_page.html'
#     extra_context = {'title': 'Проведенные аукционы'}
#
#     def get_queryset(self):
#         return Car.objects.all().select_related('car_model', 'engine', 'car_model__manufacturer')

def main_page_list_of_auctions(request):
    """Список всех проданных автомобилей"""
    list_of_car_pk = []
    object_list = Car.objects.all()[:10].select_related('car_model', 'engine', 'car_model__manufacturer')
    for car in object_list:
        list_of_car_pk.append(car.pk)
    car_images = Images.objects.filter(car__in=list_of_car_pk).select_related('car')
    context = {
        'object_list': object_list,
        'car_images': car_images,
        'title': 'Проведенные аукционы',
        'list_of_car_pk': list_of_car_pk
    }
    return render(request, template_name='auction/main_page.html', context=context)


class DetailOfAuctions(DetailView):
    """Подробная информация о проданном автомобиле"""
    model = Car
    template_name = 'auction/car_detail.html'
    extra_context = {'title': f'Проведенный аукцион'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_photos'] = self.get_object().images_set.all().select_related('car')
        context['cnt_photos'] = list(range(len(context['car_photos'])))
        return context

    def get_queryset(self):
        return Car.objects.filter(slug=self.kwargs['slug']).select_related('car_model', 'engine', 'engine__type',
                                                                           'transmission__type', 'transmission',
                                                                           'wheel', 'car_model__manufacturer')


class FormWizard(SessionWizardView):
    """Пятиступенчатая форма добавления авто для продажи"""
    form_list = [ManufacturerAndModelWizard, EngineAndEngineTypeWizard, TransmissionAndTransmissionTypeWizard,
                 WheelTypeWizard, CarWizard]
    template_name = 'auction/sell_form_wizard.html'
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'form-photos-storage'))

    def done(self, form_list, **kwargs):
        """Сохранение проверенных данных"""
        model_and_manufacturer = form_list[0].cleaned_data
        engine_and_engine_type = form_list[1].cleaned_data
        transmission_wizard = form_list[2].cleaned_data
        wheel_wizard = form_list[3].cleaned_data
        car_wizard = form_list[4].cleaned_data

        if len(CarModel.objects.filter(name=model_and_manufacturer['name'])) == 0:
            # проверка модели авто на уникальность
            step1 = CarModel.objects.create(
                name=model_and_manufacturer['name'],
                manufacturer=model_and_manufacturer['manufacturer']
            )
        else:
            step1 = None
        step2 = Engine.objects.create(
            volume=engine_and_engine_type['volume'],
            power=engine_and_engine_type['power'],
            type=engine_and_engine_type['type']
        )
        step3 = Transmission.objects.create(
            speed_cnt=transmission_wizard['speed_cnt'],
            type=transmission_wizard['type'],
        )
        step5 = Car.objects.create(
            release_date=car_wizard['release_date'],
            mileage=car_wizard['mileage'],
            sell_price=car_wizard['sell_price'],
            first_price=0,
            description=car_wizard['description'],
            slug='{}-{}-{}-{}'.format(model_and_manufacturer['manufacturer'], model_and_manufacturer['name'],
                                      car_wizard['release_date'], randint(1, 1000000)),
            car_model=(
                lambda no_name_func: step1 if step1 else CarModel.objects.get(name=model_and_manufacturer['name']))(
                step1),
            engine=step2,
            transmission=step3,
            wheel=Wheel.objects.get(name=wheel_wizard['name'])
        )

        return HttpResponseRedirect(reverse('success'))


class RegisterBaseUser(CreateView):
    """Создание рядового пользователя"""
    form_class = OurUserCreationForm
    template_name = 'auction/register_users.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home_page')


class LoginBaseUser(LoginView):
    """Авторизация пользователя"""
    template_name = 'auction/login_users.html'
    form_class = OurUserAuthenticationForm

    def get_success_url(self):
        return reverse('sell_car')


def logout_user(request):
    logout(request)
    return redirect('home_page')


def success_page(request):
    return render(request, template_name='auction/success.html')
