from django.urls import path

from .views import main_page_list_of_auctions, DetailOfAuctions, FormWizard  # , ListOfAuctions

urlpatterns = [
    # path('', ListOfAuctions.as_view(), name='home_page'),
    path('', main_page_list_of_auctions, name='home_page'),
    path('car/<slug:slug>', DetailOfAuctions.as_view(), name='car_detail'),
    path('sell-car', FormWizard.as_view(), name='sell_car'),
]
