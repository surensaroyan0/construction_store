from django.views import View
from django.shortcuts import render
from django.contrib import messages

from .authentication import auth
from .user import StoreUser
from ..models.order import Order


class OrderView(View):
    def get(self, request):
        is_auth, context = auth(request)

        if is_auth:
            try:
                user = StoreUser.objects.get(user__username=context["store_user"]["username"])
                order_items = Order.objects.filter(user=user)
                context["cart_items"] = order_items
            except StoreUser.DoesNotExist:
                messages.error(request, "User not found.")

        return render(request, "construction_store/order.html", context)