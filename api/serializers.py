from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Stock, Watchlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "symbol", "name", "stock_img_url", "price", "created_at"]

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["id", "name", "user", "stocks", "created_at"]

        extra_kwargs = {"user": {"read_only": True}, "stocks": {"required": False}}