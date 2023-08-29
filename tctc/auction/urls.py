from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import main_page_list_of_auctions, DetailOfAuctions, FormWizard, RegisterBaseUser, LoginBaseUser, \
    logout_user, success_page, info_page, lk

urlpatterns = [
    path('', main_page_list_of_auctions, name='home_page'),
    path('car/<slug:slug>', cache_page(10)(DetailOfAuctions.as_view()), name='car_detail'),
    path('sell-car/', FormWizard.as_view(), name='sell_car'),
    path('register-user/', RegisterBaseUser.as_view(), name='register'),
    path('login-user/', LoginBaseUser.as_view(), name='login'),
    path('logout-user/', logout_user, name='logout'),
    path('success/', success_page, name='success'),
    path('info-page/', info_page, name='info_page'),
    path('personal-page/', lk, name='personal_page'),
    #path('personal-area/', , name='lk'),
]
