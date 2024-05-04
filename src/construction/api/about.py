from django.shortcuts import render
from django.views import View
from .authentication import auth


class AboutView(View):
    def get(self, request):
        is_auth, context = auth(request)
        return render(request, "construction_store/about.html", context)