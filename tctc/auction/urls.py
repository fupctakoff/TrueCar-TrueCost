from django.urls import path
from .views import ListOfAuctions, DetailOfAuctions

urlpatterns = [
    path('', ListOfAuctions.as_view(), name='home_page'),
    path('<slug:slug>', DetailOfAuctions.as_view(), name='car_detail'),
]
