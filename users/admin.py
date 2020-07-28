
from .models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    ordering = ('-date_joined', )
    list_display = ('username', 'email', 'date_joined',
                    'last_login', 'is_active')  # Added last_login


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Profile)
