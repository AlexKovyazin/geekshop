from django.contrib import admin

from users.models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active',)
    ordering = ('username',)
    search_fields = ('id', 'username', 'email', 'is_staff', 'is_active',)
    # fields = ()
