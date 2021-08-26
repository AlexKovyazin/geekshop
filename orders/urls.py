from django.urls import path
from geekshop import settings
from django.conf.urls.static import static

from orders.views import OrdersList, AdminOrdersList

app_name = 'orders'

urlpatterns = [
    path('orders/', OrdersList.as_view(), name='OrdersList'),
    path('admin/orders', AdminOrdersList.as_view(), name='AdminOrdersList'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
