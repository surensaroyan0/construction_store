import stripe

from django.conf import settings
from django.views import View
from django.shortcuts import redirect, render, reverse

from ..api.authentication import auth
from ..models.product import Product
from ..api.product import context_func

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
        quantity = request.POST["quantity"]
        product_id = self.kwargs["id"]
        product = Product.objects.get(id=product_id)
        domain_url = 'http://127.0.0.1:8000/payment/'

        session_data = {
            'payment_method_types': ['card'],
            'line_items': [{
                    'price_data': {
                        'currency': 'amd',
                        'unit_amount': product.price * 100,
                        'product_data': {'name': product.name}
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
            # session_data['customer_card_number'] = request.session.get("card_number")
            # session_data['customer_cardholder_name'] = request.session.get("cardholder_name")
            # session_data['customer_card_expiration'] = request.session.get("card_expiration")
            # session_data['customer_card_cvv'] = request.session.get("card_cvv")

        checkout_session = stripe.checkout.Session.create(**session_data)
        return redirect(checkout_session.url, code=303)


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        # if not self.payment_successful(request):
        #     return redirect(reverse('failure_url'))

        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse("login"))

        return render(request, "payment/success.html", context)


class CancelView(View):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse("login"))

        return render(request, "payment/cancel.html", context)
