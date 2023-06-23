from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, documet_root=settings.MEDIA_ROOT)
