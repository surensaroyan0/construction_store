from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone


from ..models.payment_card import Card
from ..models.user import StoreUser
from .authentication import auth


def clean(year, month):
    if year == timezone.now().year and month < timezone.now().month:
        return "Expiration month cannot be in the past for the current year."
    return False


class PaymentCardView(View):
    def post(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse('login'))

        user_id = context["store_user"]["id"]

        try:
            username = context["store_user"]["username"]
            card_number = request.POST["card_number"]
            cardholder_name = request.POST["cardholder_name"]
            expiration_month = request.POST["expiration_month"]
            expiration_year = request.POST["expiration_year"]
            cvv = request.POST["cvv"]
            expiration = clean(expiration_year, expiration_month)

            if expiration:
                context["expiration"] = expiration
                return render(request, "construction_store/profile.html", context)

            store_user = StoreUser.objects.get(user__username=username)
            Card.objects.create(user=store_user, card_number=card_number, cardholder_name=cardholder_name,
                                expiration_month=expiration_month, expiration_year=expiration_year, cvv=cvv)
            messages.success(request, 'Payment card added successfully.')
        except KeyError:
            messages.error(request, 'Incomplete data. Please fill all required fields.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return HttpResponseRedirect(f"/api/user/profile/{user_id}/")
