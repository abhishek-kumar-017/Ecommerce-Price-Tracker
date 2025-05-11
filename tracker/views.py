from rest_framework import generics, filters
from .models import Product, PriceHistory
from .serializers import ProductSerializer, PriceHistorySerializer


# List & Search products
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-last_updated')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'seller__name']


# Get price history for a specific product
class ProductPriceHistoryView(generics.ListAPIView):
    serializer_class = PriceHistorySerializer

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return PriceHistory.objects.filter(
            product_id=product_id).order_by('-checked_at')
