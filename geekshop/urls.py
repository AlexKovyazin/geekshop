from django.contrib import admin
from django.urls import path, include
from geekshop import settings
from django.conf.urls.static import static

from products.views import ProductsIndexView

urlpatterns = [
    path('', ProductsIndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('userAdmin/', include('userAdmin.urls', namespace='userAdmin')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
