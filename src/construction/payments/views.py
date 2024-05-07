import stripe

from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, render

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
        domain_url = 'http://127.0.0.1.8000'

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
            'success_url': domain_url + '/success/',
            'cancel_url': domain_url + '/cancel/',
            'locale': 'en'
        }
        if is_auth:
            session_data['customer_email'] = context["store_user"]["email"]

        checkout_session = stripe.checkout.Session.create(**session_data)
        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
