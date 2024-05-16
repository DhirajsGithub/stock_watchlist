from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, WatchlistSerializer, StockSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Watchlist, Stock
from rest_framework.response import Response


class CreateUserView(generics.CreateAPIView):
   
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class GetUserInfo(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    

# create a watchlist
class WatchlistListCreate(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchlistAddStock(generics.UpdateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        watchlist = self.get_object()
        stock_data = request.data.get("stock")
        stock_serializer = StockSerializer(data=stock_data)
        if stock_serializer.is_valid():
            stock = stock_serializer.save()
        else:
            return Response(stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        watchlist.stocks.add(stock)
        watchlist.save()

        return Response({'status': 'stock added'}, status=status.HTTP_200_OK)
    

# get all stocks of a specific watchlist
class WatchlistGetStocks(generics.ListAPIView):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        watchlist_id = self.kwargs.get('pk')
        try:
            watchlist = Watchlist.objects.get(id=watchlist_id)
            return watchlist.stocks.all()
        except Watchlist.DoesNotExist:
            return Stock.objects.none() 



# remove a stock from a watchlist
class WatchlistRemoveStock(generics.GenericAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        stock_id = request.data.get('stock_id')
        watchlist_id = request.data.get('watchlist_id')

        if stock_id is not None and watchlist_id is not None:
            try:
                stock = Stock.objects.get(id=stock_id)
                watchlist = Watchlist.objects.get(id=watchlist_id)
                watchlist.stocks.remove(stock)
                watchlist.save()
                return Response({'status': 'stock removed'}, status=status.HTTP_200_OK)
            except Stock.DoesNotExist:
                return Response({"error": "Stock does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Watchlist.DoesNotExist:
                return Response({"error": "Watchlist does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Missing stock_id or watchlist_id"}, status=status.HTTP_400_BAD_REQUEST)
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Watchlist.objects.filter(user=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            stock_id = serializer.validated_data.get('stock_id')
            watchlist_id = serializer.validated_data.get('watchlist_id')

            try:
                stock = Stock.objects.get(id=stock_id)
                watchlist = Watchlist.objects.get(id=watchlist_id)
                watchlist.stocks.remove(stock)
                watchlist.save()
            except Stock.DoesNotExist:
                print("Stock does not exist")
            except Watchlist.DoesNotExist:
                print("Watchlist does not exist")
        else:
            print(serializer.errors)


# delete a specific watchlist
class WatchlistDelete(generics.DestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]
    queryset = Watchlist.objects.all()

    def get_object(self):
        user = self.request.user
        watchlist_id = self.kwargs.get('pk') 
        return Watchlist.objects.get(user=user, id=watchlist_id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Watchlist deleted!!!'}, status=status.HTTP_204_NO_CONTENT)
    
# get all watchlists of a specific user with stocks in
class WatchlistGetAll(generics.ListAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Watchlist.objects.filter(user=user)
    
