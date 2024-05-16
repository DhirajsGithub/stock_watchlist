from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    stock_img_url = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    stocks = models.ManyToManyField(Stock, related_name="watchlists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
