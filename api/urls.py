from django.urls import path

from .views import CategoryCBV, CategoryDetailCBV, ProjectCBV, ProjectDetailCBV

urlpatterns = [
    path("categories/", CategoryCBV.as_view(), name="category-list"),
    path("categories/<uuid:pk>/", CategoryDetailCBV.as_view(), name="category-detail"),
    path("projects/", ProjectCBV.as_view(), name="project-list"),
    path("projects/<uuid:pk>/", ProjectDetailCBV.as_view(), name="project-detail"),
]
