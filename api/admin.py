from django.contrib import admin

from .models import Category, Project, Task


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at", "updated_at")
    search_fields = ("title", "owner__username")
    list_filter = ("created_at", "updated_at")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "owner", "created_at", "updated_at")
    search_fields = ("title", "category__title", "owner__username")
    list_filter = ("created_at", "updated_at")


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "importance_level",
        "project",
        "assigned_to",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "project__title", "assigned_to__username")
    list_filter = ("status", "importance_level", "created_at", "updated_at")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
