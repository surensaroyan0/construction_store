import string
import random

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, logout
from django.conf import settings
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from ..models.user import StoreUser
from ..models.apikey import ApiKey

static_url = settings.STATIC_URL_PREFIX


class UserView(View):
    @staticmethod
    def login(request):
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

            subject = f"Dear {user.username}"
            message = (f"Welcome to BuildSupply Co! We are excited to have you as a member of our community.\n\n"
                       f"Your account has been successfully registered, and you can now access all the features and "
                       f"benefits of our platform. Whether you're looking for top-quality construction materials or "
                       f"tools for your projects, we've got you covered.\n\n"
                       f"If you have any questions or need assistance, feel free to reach out to our support team at "
                       f"suren.saroyannn@gmail.com. We're here to help!\n\n"
                       f"Thank you for choosing BuildSupply Co. We look forward to serving you.\n\n"
                       f"Best regards,\n"
                       f"The BuildSupply Co Team\n\n"
                       f"BuildSupply Co\n"
                       f"localhost:8000/api/home/\n"
                       f"suren.saroyannn@gmail.com")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            return HttpResponseRedirect("/api/user/login/")

    @staticmethod
    def log_out(request):
        logout(request)

        return HttpResponseRedirect("/api/home/")

    @staticmethod
    def delete(request, *args, **kwargs):
        store_user = StoreUser.objects.get(pk=kwargs["id"])
        user_id = store_user.user_id
        user = User.objects.get(pk=user_id)
        user.delete()

        return HttpResponseRedirect("/api/home/")

    @staticmethod
    def forgot_password(request, *args, **kwargs):
        context = {"STATIC_URL": static_url}

        if request.method == "GET":
            return render(request, "construction_store/forgot_password.html", context)
        else:
            number_or_email = request.POST["number_or_email"]
            user = User.objects.get(email=number_or_email)
            pin_code = random.randrange(100000, 999999)
            request.session["pin_code"] = pin_code
            request.session["email"] = number_or_email

            subject = f"{user.username}, your PIN code is - {pin_code}"
            message = f"Your PIN code is {pin_code}."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            return render(request, "construction_store/confirm_code.html", context)

    @staticmethod
    def confirm_code(request, *args, **kwargs):
        context = {"STATIC_URL": static_url}

        pin_code = int(request.POST["pin_code"])

        if pin_code == request.session["pin_code"]:
            return render(request, "construction_store/change_password.html", context)
        else:
            context["error"] = "Incorrect PIN code"
            return render(request, "construction_store/confirm_code.html", context)

    @staticmethod
    def change_password(request, *args, **kwargs):
        password = request.POST["password"]

        user = User.objects.get(email=request.session["email"])
        user.password = make_password(password)
        user.save()

        return redirect(reverse("login"))
