from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'role', 'monitor_hosts', 'monitor_containers')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'email', 'role', 'monitor_hosts', 'monitor_containers')}),
    )

    list_display = ['username', 'name', 'email', 'role', 'is_staff', 'is_active']
    search_fields = ['username', 'name', 'email']

admin.site.register(CustomUser, CustomUserAdmin)
