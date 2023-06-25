from django.urls import path
from .views import ListOfAuctions


urlpatterns = [
    path('', ListOfAuctions.as_view(), name='home_page'),
]
