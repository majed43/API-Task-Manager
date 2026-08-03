from django.urls import path

from .views import (
    CategoryCBV,
    CategoryDetailCBV,
    ProjectCBV,
    ProjectDetailCBV,
    TaskByProjectCBV,
    TaskCBV,
    TaskDetailCBV,
)

urlpatterns = [
    path("categories/", CategoryCBV.as_view(), name="category-list"),
    path("categories/<uuid:pk>/", CategoryDetailCBV.as_view(), name="category-detail"),
    path("projects/", ProjectCBV.as_view(), name="project-list"),
    path("projects/<uuid:pk>/", ProjectDetailCBV.as_view(), name="project-detail"),
    path(
        "projects/<slug:slug>/tasks/",
        TaskByProjectCBV.as_view(),
        name="task-by-project",
    ),
    path("tasks/", TaskCBV.as_view(), name="task-list"),
    path("tasks/<uuid:pk>/", TaskDetailCBV.as_view(), name="task-detail"),
]
