from rest_framework import generics
from .models import Product, PriceHistory
from .serializers import ProductSerializer, PriceHistorySerializer


class ProductListView(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
        # keyword = self.request.query_params.get('search')
        # if keyword:
        #     return self.queryset.filter(title__icontains=keyword)
        # return self.queryset


class ProductPriceHistoryView(generics.ListAPIView):
    serializer_class = PriceHistorySerializer

    def get_queryset(self):
        return PriceHistory.objects.filter(product_id=self.kwargs['pk'])
