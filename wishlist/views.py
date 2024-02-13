from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Product, Profile, Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from rest_framework.response import Response
from store.serializers import WishlistSerializer
from rest_framework import viewsets, response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status


class RemoveFromWishlistView(View):
    def get(self, request, product_id):
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
        except Wishlist.DoesNotExist:
            return redirect('wishlist:wishlist')

        wishlist_item.delete()

        return redirect('wishlist:wishlist')


class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user)
            return render(request, "wishlist/wishlist.html", {'wishlist': wishlist})
        else:
            return redirect('login:login')


class AddToWishlistView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return HttpResponseNotAllowed(['POST'])

    def post(self, request, product_id):
        print("Received product_id:", product_id)
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=product_id)
            wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
            if wishlist_item.exists():
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                wishlist_item = Wishlist.objects.create(user=request.user, product=product)
                wishlist_item.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseRedirect('/login/')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        wishlist_items = self.get_queryset().filter(product_id=product_id)
        if wishlist_items.exists():
            return Response({'message': 'Product already in wishlist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            product = get_object_or_404(Product, id=product_id)
            wishlist_item = Wishlist(user=request.user, product=product)
            wishlist_item.save()
            return Response({'message': 'Product added to wishlist'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        wishlist_item = get_object_or_404(Wishlist, id=kwargs['pk'])
        product = get_object_or_404(Product, id=request.data['product'])
        wishlist_item.product = product
        wishlist_item.save()
        return Response({'message': 'Product updated in wishlist'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        wishlist_item = self.get_queryset().get(id=kwargs['pk'])
        wishlist_item.delete()
        return Response({'message': 'Product deleted from wishlist'}, status=status.HTTP_204_NO_CONTENT)
