import os

from django.views.generic import DetailView
from django.shortcuts import render
from .authentication import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect, reverse

from ..models.user import StoreUser
from ..models.payment_card import Card


class ProfileDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            return redirect(reverse('login'))

        store_user = StoreUser.objects.get(pk=kwargs["id"])
        payment_cards = Card.objects.filter(user=store_user)
        context["store_user"] = store_user.to_dict()
        context["payment_cards"] = [card.to_dict() for card in payment_cards]

        return render(request, "construction_store/profile.html", context)

    def post(self, request, *args, **kwargs):
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST["username"]
        request.session["username"] = username
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        gender = request.POST.get("gender")
        phone_number = request.POST["phone_number"]
        is_main = request.POST.get("main")
        card_id = request.POST["card_id"]
        card_number = request.POST["added_card_number"]
        cardholder_name = request.POST["added_cardholder_name"]
        card_expiration = request.POST["added_expiration"]
        card_cvv = request.POST["added_cvv"]

        store_user = StoreUser.objects.get(pk=kwargs["id"])

        if is_main:
            card = Card.objects.get(user=store_user, pk=card_id)
            cards = Card.objects.filter(user=store_user)
            for card in cards:
                card.is_main = False

            card.is_main = True
            card.save()
            request.session["card_number"] = card_number
            request.session["cardholder_name"] = cardholder_name
            request.session["card_expiration"] = card_expiration
            request.session["card_cvv"] = card_cvv

        if profile_picture and profile_picture != store_user.profile_picture:
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profile'))
            filename = fs.save(profile_picture.name, profile_picture)
            profile_picture_url = fs.url(os.path.join('profile', filename))
            store_user.profile_picture = profile_picture_url

        store_user.user.username = username
        store_user.user.first_name = firstname
        store_user.user.last_name = lastname
        store_user.user.email = email
        if gender:
            store_user.gender = gender
        store_user.phone_number = phone_number
        store_user.user.save()
        store_user.save()

        return HttpResponseRedirect(f"/api/user/profile/{kwargs['id']}/")
