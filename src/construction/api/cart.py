from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse

from .authentication import auth
from ..models.cart import Cart
from ..models.product import Product
from ..models.user import StoreUser


class CartView(View):
    def get(self, request):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse('login'))

        user = StoreUser.objects.get(user__username=context["store_user"]["username"])
        cart_items = Cart.objects.filter(user=user)
        context["cart_items"] = cart_items

        return render(request, "construction_store/cart.html", context)

    def post(self, request):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse('login'))

        try:
            quantity = request.POST["quantity"]
            product_id = request.POST["product_id"]
            product = Product.objects.get(pk=product_id)
            try:
                store_user = StoreUser.objects.get(user__username=context["store_user"]["username"])
                Cart.objects.get(user=store_user, product=product)
            except Cart.MultipleObjectsReturned:
                messages.success(request, "Product is already added in cart.")
            except Cart.DoesNotExist:
                Cart.objects.create(user=store_user, product=product, quantity=quantity)
                messages.success(request, "Product added to cart successfully.")
            else:
                messages.success(request, "Something went wrong.")
        except KeyError:
            messages.error(request, "Product ID not provided.")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

        return HttpResponseRedirect("/api/cart/")

    @staticmethod
    def delete(request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse('login'))

        store_user = StoreUser.objects.get(user__username=context["store_user"]["username"])

        try:
            product = Product.objects.get(pk=kwargs["product_id"])
            Cart.objects.get(user=store_user, product=product).delete()
            messages.success(request, "Product removed from cart successfully.")
        except KeyError:
            messages.error(request, "Product ID not provided.")
            messages.error(request, "Product ID not provided.")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

        return HttpResponseRedirect("/api/cart/")
