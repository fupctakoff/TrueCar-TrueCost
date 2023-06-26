from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Car


class ListOfAuctions(ListView):
    """Список всех проданных автомобилей"""
    model = Car
    template_name = 'auction/main_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # c = Car.objects.get(slug=self.kwargs['slug'])
        print(self.kwargs)
        # context['car_photo'] =
        return context
    def get_queryset(self):
        return Car.objects.all().select_related('car_model', 'engine', 'car_model__manufacturer')


class DetailOfAuctions(DetailView):
    """Подробная информация о проданном автомобиле"""
    model = Car
    template_name = 'auction/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_photos'] = self.get_object().images_set.all().select_related('car')
        context['cnt_photos'] = list(range(len(context['car_photos'])))
        print(context['car_photos'])
        return context

    def get_queryset(self):
        return Car.objects.filter(slug=self.kwargs['slug']).select_related('car_model', 'engine', 'engine__type',
                                                                           'transmission__type', 'transmission', \
                                                                           'wheel', 'car_model__manufacturer')
