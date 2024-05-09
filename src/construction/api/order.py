from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .authentication import auth
from .user import StoreUser
from ..models.order import Order


class OrderView(View):
    def get(self, request):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse("login"))

        user = StoreUser.objects.get(user__username=context["store_user"]["username"])
        order_items = Order.objects.filter(user=user)
        context["cart_items"] = order_items

        return render(request, "construction_store/order.html", context)
