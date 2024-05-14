from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title
    
# The platform should allow users to create and manage their own watchlists of stock symbols
# (e.g., MSFT, GOOG).
# • The platform should display a dashboard with the latest stock values of the symbols on the
# user’s watchlist.
# • The platform should be able to handle multiple users concurrently, each having different
# watchlists.

# a user can have multiple watchlists
# a watchlist can have multiple stock symbols

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
    
# The platform should allow users to create and manage their own watchlists of stock symbols
    
