from django.urls import path
from .views import ProductListView, ProductPriceHistoryView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/history/',
         ProductPriceHistoryView.as_view(),
         name='product-history'),
]
