from django.urls import path
from .views import WishlistView, RemoveFromWishlistView, AddToWishlistView

app_name = 'wishlist'

urlpatterns = [
    path('delete/<int:product_id>/', RemoveFromWishlistView.as_view(), name='delete_from_wishlist'),
    path('', WishlistView.as_view(), name='wishlist'),
    path('add/<int:product_id>/', AddToWishlistView.as_view(), name='add_to_wishlist'),
]