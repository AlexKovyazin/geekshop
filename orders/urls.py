from django.contrib import admin
from django.urls import path, include
from geekshop import settings
from django.conf.urls.static import static

app_name = 'orders'

urlpatterns = [

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
