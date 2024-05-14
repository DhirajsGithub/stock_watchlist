from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Stock, Watchlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


# The platform should allow users to create and manage their own watchlists of stock symbols
# (e.g., MSFT, GOOG).
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "symbol", "name", "stock_img_url", "price", "created_at"]

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["id", "name", "user", "stocks", "created_at"]

        extra_kwargs = {"user": {"read_only": True}, "stocks": {"required": False}}