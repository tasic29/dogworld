from django.contrib import admin
from .models import MyUser, UserProfile


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username',
                    'first_name', 'last_name', 'location']
    search_fields = ['email', 'username', 'first_name', 'last_name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user__first_name',
                    'user__last_name',   'location', 'joined']
    search_fields = ['user__email', 'user__username', 'location']
    list_filter = ['joined']
