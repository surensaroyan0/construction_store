from django.conf import settings

from ..models.user import StoreUser
from ..models.apikey import ApiKey


def auth(request):
    context = {"STATIC_URL": settings.STATIC_URL_PREFIX}
    try:
        username = request.session["username"]
        api_key = request.session["api_key"]
    except KeyError:
        username = ""
        api_key = ""
    is_auth = True

    try:
        store_user = StoreUser.objects.get(user__username=username)
        ApiKey.objects.get(user=store_user, api_key=api_key)
    except StoreUser.DoesNotExist:
        is_auth = False
        context["error"] = "User not found with given username"
    except ApiKey.DoesNotExist:
        is_auth = False
        context["error"] = "ApiKey does not match"
    else:
        context['store_user'] = store_user.to_dict()

    return is_auth, context
