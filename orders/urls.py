from django.urls import path
from geekshop import settings
from django.conf.urls.static import static

from orders.views import OrdersList, OrderItemsCreate, OrderRead, OrderUpdate, OrderDelete, \
    order_forming_complete

app_name = 'orders'

urlpatterns = [
    path('', OrdersList.as_view(), name='OrdersList'),
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('create/', OrderItemsCreate.as_view(), name='OrderItemsCreate'),
    path('read/<int:pk>/', OrderRead.as_view(), name='OrderRead'),
    path('update/<int:pk>/', OrderUpdate.as_view(), name='OrderUpdate'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='OrderDelete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
