from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import logout

from .authentication import auth
from .order import Order


class PurchaseView(View):
    def get(self, request):
        is_auth, context = auth(request)

        if not is_auth:
            logout(request)
            return redirect(reverse("login"))

        bought_items = Order.objects.filter(status=5)
        context["bought_items"] = [bought_item.to_dict() for bought_item in bought_items]

        return render(request, "construction_store/purchase.html", context)
