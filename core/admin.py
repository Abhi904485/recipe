from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Recipe


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('email', 'name')
    fieldsets = (
        (_('Basic'), {'fields': ('email', 'password')}),
        (_('Permission'), {'fields': ('is_active',
                                      'is_staff',
                                      'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ('last_login',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Recipe._meta.get_fields()]
