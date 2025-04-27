from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Watch

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'user')
    search_fields = ('device_id', 'user__username')

