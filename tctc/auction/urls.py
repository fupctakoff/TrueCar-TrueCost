from django.urls import path, include

from .views import main_page_list_of_auctions, DetailOfAuctions, FormWizard, RegisterBaseUser, LoginBaseUser, \
    logout_user, success_page

urlpatterns = [
    path('', main_page_list_of_auctions, name='home_page'),
    path('car/<slug:slug>', DetailOfAuctions.as_view(), name='car_detail'),
    path('sell-car/', FormWizard.as_view(), name='sell_car'),
    path('register-user/', RegisterBaseUser.as_view(), name='register'),
    path('login-user/', LoginBaseUser.as_view(), name='login'),
    path('logout-user/', logout_user, name='logout'),
    path('success/', success_page, name='success'),
    #path('personal-area/', , name='lk'),
]
