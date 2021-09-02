from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'updated', 'status', 'is_active')
    fields = ('user', 'status')
    ordering = ('-updated',)
