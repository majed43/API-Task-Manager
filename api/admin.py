from django.contrib import admin

from .models import Category, Project, Task

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Task)
