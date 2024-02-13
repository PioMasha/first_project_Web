from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from store.models import Product, Profile, Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed, HttpResponseRedirect


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
