from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/delete/<int:pk>/", views.NoteDelete.as_view(), name="delete-note"),

    # path for creating a watchlist
    path("watchlist/", views.WatchlistListCreate.as_view(), name="watchlist-list"),

    # path for adding a stock to a watchlist
    path("watchlist/addstock/<int:pk>", views.WatchlistAddStock.as_view(), name="watchlist-add-stock"),

    # path for getting all stocks of a specific watchlist
    path("watchlist/getstocks/<int:pk>", views.WatchlistGetStocks.as_view(), name="watchlist-get-stocks"),

    # path for removing a stock from a watchlist
    path("watchlist/removestock/", views.WatchlistRemoveStock.as_view(), name="watchlist-remove-stock"),

    # path for deleting a watchlist
    path("watchlist/deletewatchlist/<int:pk>", views.WatchlistDelete.as_view(), name="watchlist-delete"),

    # path for getting all watchlists of a user 
    path("watchlist/getwatchlists/", views.WatchlistGetAll.as_view(), name="watchlist-get-all"),

]