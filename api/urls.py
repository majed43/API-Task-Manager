from django.urls import path
from .views import CategoryCBV, CategoryDetailCBV

urlpatterns = [
    path("categories/", CategoryCBV.as_view(), name="category-list"),
    path("categories/<uuid:pk>/", CategoryDetailCBV.as_view(), name="category-detail"),
]
