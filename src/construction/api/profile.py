import os

from django.views.generic import DetailView
from django.shortcuts import render
from .authentication import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from ..models.user import StoreUser


class ProfileDetailView(DetailView):
    def get(self, request, id):
        is_auth, context = auth(request)

        if is_auth:
            if id == context["store_user"]["id"]:
                try:
                    store_user = StoreUser.objects.get(pk=id)
                    context["store_user"] = store_user.to_dict()
                except StoreUser.DoesNotExist:
                    context["error_message"] = "User not found"
            else:
                context["error_message"] = "Unauthorized access"

        return render(request, "construction_store/profile.html", context)

    def post(self, request, id):
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        gender = request.POST.get("gender")
        phone_number = request.POST["phone_number"]
        store_user = StoreUser.objects.get(pk=id)

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

        return HttpResponseRedirect(f"/api/user/profile/{id}")

    @staticmethod
    def delete(request, id):
        store_user = StoreUser.objects.get(pk=id)
        user_id = store_user.user_id
        user = User.objects.get(pk=user_id)
        user.delete()
        return HttpResponseRedirect("/api/home/")
