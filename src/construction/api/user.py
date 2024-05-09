import string
import random

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, logout
from django.conf import settings
from django.views import View
from django.core.mail import send_mail

from ..models.user import StoreUser
from ..models.apikey import ApiKey


class UserView(View):
    @staticmethod
    def login(request):
        static_url = settings.STATIC_URL_PREFIX
        context = {"STATIC_URL": static_url}
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(username=username, password=password)

            if user:
                store_user = StoreUser.objects.get(user=user)
                api_key = ApiKey.objects.get(user=store_user)

                request.session["id"] = store_user.id
                request.session["username"] = user.username
                request.session["api_key"] = api_key.api_key
                return HttpResponseRedirect("/api/home/")
            context["error"] = "Wrong username or password"
        return render(request, "construction_store/login.html", context)

    @staticmethod
    def register(request):
        static_url = settings.STATIC_URL_PREFIX
        if request.method == "GET":
            return render(request, "construction_store/registration.html",
                          {"STATIC_URL": static_url})
        else:
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]

            user = User.objects.create_user(username=username, password=password, email=email)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            store_user = StoreUser(user=user)
            store_user.save()
            ApiKey(user=store_user, api_key=''.join(random.choice(string.ascii_letters) for _ in range(16))).save()

            subject = "Something"
            message = f"Hi {user.username}, thank you for registering in BuildSupply CO."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)
            return HttpResponseRedirect("/api/user/login/")

    @staticmethod
    def log_out(request):
        logout(request)
        return HttpResponseRedirect("/api/home/")
