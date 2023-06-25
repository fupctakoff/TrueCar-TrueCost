from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Car


class ListOfAuctions(ListView):
    model = Car
    template_name = 'auction/main_page.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context