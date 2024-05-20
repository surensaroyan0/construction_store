from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout

from .authentication import auth
from .user import StoreUser
from ..models.order import Order


class OrderView(View):
    def get(self, request):
        is_auth, context = auth(request)

        if not is_auth:
            logout(request)
            return redirect(reverse("login"))

        user = StoreUser.objects.get(user__username=context["store_user"]["username"])
        order_items = Order.objects.filter(user=user).exclude(status=5)
        for order_item in order_items:
            order_item.status = order_item.get_status_display()
        context["order_items"] = order_items

        return render(request, "construction_store/order.html", context)
