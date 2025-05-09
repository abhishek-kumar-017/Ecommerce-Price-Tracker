from rest_framework import serializers
from .models import Product, PriceHistory


class PriceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PriceHistory
        fields = ['price', 'timestamp']


class ProductSerializer(serializers.ModelSerializer):
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'current_price', 'rating', 'num_reviews', 'seller',
            'url', 'price_history'
        ]
