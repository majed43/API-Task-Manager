from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering = ("-joined_at",)
    readonly_fields = ("joined_at", "updated_at")


admin.site.register(User, UserAdmin)
