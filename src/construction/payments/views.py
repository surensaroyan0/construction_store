import stripe

from django.conf import settings
from django.views import View
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import User

from ..api.authentication import auth
from ..models.product import Product
from ..api.product import context_func
from ..models.order import Order
from ..models.user import StoreUser

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)
        context.update(context_func())
        product = Product.objects.get(pk=kwargs.get('id')).to_dict()
        product["specifications"] = product["specifications"].replace("․", "").split(", ")
        context["product"] = product
        context["STRIPE_PUBLISHABLE_KEY"]: settings.STRIPE_PUBLISHABLE_KEY
        return render(request, "payment/landing.html", context)

    def post(self, request, *args, **kwargs):
        is_auth, context = auth(request)
        quantity = int(request.POST["quantity"])
        product = Product.objects.get(id=self.kwargs["id"])
        domain_url = 'http://127.0.0.1:8000/payment/'

        request.session["product_id"] = self.kwargs["id"]
        request.session["product_quantity"] = quantity
        request.session["product_price"] = product.price * quantity

        session_data = {
            'payment_method_types': ['card'],
            'line_items': [{
                    'price_data': {
                        'currency': 'amd',
                        'unit_amount': product.price * 100,
                        'product_data': {
                            'name': product.name,
                            'images': [f"http://127.0.0.1:8000/{product.image.url}"]
                        }
                    },
                    'quantity': quantity,
                }],
            'mode': 'payment',
            'success_url': domain_url + 'success/',
            'cancel_url': domain_url + 'cancel/',
            'locale': 'en'
        }
        if is_auth:
            session_data['customer_email'] = context["store_user"]["email"]

        checkout_session = stripe.checkout.Session.create(**session_data)

        return redirect(checkout_session.url, code=303)


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse("login"))

        user = User.objects.get(username=context["store_user"]["username"])
        store_user = StoreUser.objects.get(user=user)
        product = Product.objects.get(pk=request.session["product_id"])
        Order.objects.create(
            user=store_user,
            product=product,
            quantity=request.session["product_quantity"],
            product_price=request.session["product_price"]
        )

        return render(request, "payment/success.html", context)


class CancelView(View):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse("login"))

        return render(request, "payment/cancel.html", context)
