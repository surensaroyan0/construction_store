import os

from django.views.generic import DetailView
from django.shortcuts import render
from .authentication import auth
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib.auth import logout

from ..models.user import StoreUser
from ..models.payment_card import Card


class ProfileDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        if not is_auth:
            logout(request)
            return redirect(reverse('login'))

        store_user = StoreUser.objects.get(pk=kwargs["id"])
        payment_cards = Card.objects.filter(user=store_user)
        context["store_user"] = store_user.to_dict()
        context["payment_cards"] = [card.to_dict() for card in payment_cards]

        return render(request, "construction_store/profile.html", context)

    def post(self, request, *args, **kwargs):
        is_auth, context = auth(request)

        profile_picture = request.FILES.get('profile_picture')
        username = request.POST["username"]
        request.session["username"] = username
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        gender = request.POST.get("gender")
        phone_number = request.POST["phone_number"]
        card_id = request.POST.get("card_id")

        store_user = StoreUser.objects.get(pk=kwargs["id"])

        if card_id:
            new_card = Card.objects.get(user=store_user, pk=card_id)
            all_cards = Card.objects.filter(user=store_user)

            for card in all_cards:
                card.is_main = False
                card.save()

            new_card.is_main = True
            new_card.save()

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
        phone_number_exists = StoreUser.objects.filter(phone_number=phone_number).exists()
        if phone_number_exists:
            context["error"] = "This phone number is already is use."
            return render(request, "construction_store/profile.html", context)
        store_user.phone_number = phone_number
        store_user.user.save()
        store_user.save()

        return HttpResponseRedirect(f"/api/user/profile/{kwargs['id']}/")

    # @staticmethod
    # def verify_phone(request):
    #     if request.method == "POST":
    #         verification_code = request.POST["verification_code"]
    #         new_phone_number = request.session.ger("new_phone_number")
    #
    #         client = Client(os.environ["ACCOUNT_SID"], os.environ["AUTH_TOKEN"])
    #
    #         verification_check = client.verify \
    #             .services(os.environ["TWILIO_VERIFY_SERVICE_SID"]) \
    #             .verification_checks \
    #             .create(to=new_phone_number, code=verification_code)

