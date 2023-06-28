from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import NameForm
from .models import Car, Images


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
        'title': 'Титульник',
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


def sell_car(request):
    """В разработке"""
    if request.method == 'POST':
        # если пост запрос - логика
        form = NameForm(request.POST)
        print(f'request: {request}')
        if form.is_valid():
            print(form.cleaned_data)
            print(form.is_bound)
            return HttpResponse('thx')
    else:
        # если гет запрос - пустая форма
        form = NameForm()
    return render(request, template_name='auction/sell_form.html', context={'form': form})
