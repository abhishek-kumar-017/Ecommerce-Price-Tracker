from rest_framework import serializers
from .models import Product, PriceHistory


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class PriceHistorySerializer(serializers.ModelSerializer):

    product_name = serializers.SerializerMethodField()

    class Meta:
        model = PriceHistory
        fields = ['product_name', 'price', 'checked_at']

    def get_product_name(self, obj):
        # Return the product's title associated with this price history entry
        return obj.product.title
