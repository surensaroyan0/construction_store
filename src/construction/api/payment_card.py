from django.views import View
from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User

from ..models.payment_card import Card
from ..models.user import StoreUser
from .authentication import auth


def is_month_expiration(year, month):
    if int(year) == timezone.now().year and int(month) < timezone.now().month or int(year) < timezone.now().year:
        return "Card has expired"
    return False


def is_year_expiration(year):
    if int(year) > timezone.now().year + 5:
        return "Expiration year cannot be more than 5 years"
    return False


def is_same_card(card_number, username):
    try:
        user = User.objects.get(username=username)
        Card.objects.get(user__user=user, card_number=card_number)
        return "This card is already added"
    except Card.DoesNotExist:
        return False


class PaymentCardView(View):
    def post(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        user_id = context["store_user"]["id"]

        try:
            username = context["store_user"]["username"]
            card_number = request.POST["card_number"]
            cardholder_name = request.POST["cardholder_name"]
            expiration_month = request.POST["expiration_month"]
            expiration_year = request.POST["expiration_year"]
            cvv = request.POST["cvv"]

            if is_month_expiration(expiration_year, expiration_month):
                context["error"] = is_month_expiration(expiration_year, expiration_month)
                return render(request, "construction_store/profile.html", context)
            elif is_year_expiration(expiration_year):
                context["error"] = is_year_expiration(expiration_year)
                return render(request, "construction_store/profile.html", context)
            elif is_same_card(card_number, username):
                context["error"] = is_same_card(card_number, username)
                return render(request, "construction_store/profile.html", context)

            store_user = StoreUser.objects.get(user__username=username)

            is_main = not Card.objects.filter(user=store_user).exists()

            Card.objects.create(user=store_user, card_number=card_number, cardholder_name=cardholder_name,
                                expiration_month=expiration_month, expiration_year=expiration_year[-2:],
                                cvv=cvv, is_main=is_main)

            messages.success(request, 'Payment card added successfully.')
        except KeyError:
            messages.error(request, 'Incomplete data. Please fill all required fields.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return HttpResponseRedirect(f"/api/user/profile/{user_id}/")
