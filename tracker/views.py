from rest_framework import generics
from .models import Product, PriceHistory
from .serializers import ProductSerializer, PriceHistorySerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        if 'search' in self.request.query_params:
            keyword = self.request.query_params.get('search')
            if keyword:
                return queryset.filter(title__icontains=keyword)
        return queryset


class ProductPriceHistoryView(generics.ListAPIView):
    serializer_class = PriceHistorySerializer

    def get_queryset(self):
        queryset = PriceHistory.objects.all()
        return queryset.filter(product_id=self.kwargs['pk'])
