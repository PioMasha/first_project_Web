from rest_framework import serializers
from .models import Cart, Wishlist


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

