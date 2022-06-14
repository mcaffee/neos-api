from django.contrib import admin
from accounts.models import User, CharacterSign
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        ('API', {'fields': ('api_key',)}),
    )


@admin.register(CharacterSign)
class UserAdmin(admin.ModelAdmin):
    ordering = ('user', 'character')
    list_display = ('id', 'user', 'character', 'file')
