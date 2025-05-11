from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductListView, ProductPriceHistoryView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/history/',
         ProductPriceHistoryView.as_view(),
         name='product-history'),
]
