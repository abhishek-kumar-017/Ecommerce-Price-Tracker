from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=500)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(null=True, blank=True)
    num_reviews = models.IntegerField(null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    url = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)


class PriceHistory(models.Model):
    product = models.ForeignKey(Product,
                                related_name='price_history',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
