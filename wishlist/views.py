from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from store.models import Product, Profile, Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, HttpResponseRedirect


class RemoveFromWishlistView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('wishlist:wishlist')

        request.user.wishlist.remove(product)

        return redirect('wishlist:wishlist')


class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            wishlist_products = profile.wishlist.all()
            return render(request, "wishlist/wishlist.html", {'wishlist_products': wishlist_products})
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
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        print("HTTP_REFERER:", request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])
