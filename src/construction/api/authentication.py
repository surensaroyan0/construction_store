from django.conf import settings

from ..models.user import StoreUser
from ..models.apikey import ApiKey


def auth(request):
    context = {"STATIC_URL": settings.STATIC_URL_PREFIX}
    try:
        username = request.session["username"]
        api_key = request.session["api_key"]

        try:
            store_user = StoreUser.objects.get(user__username=username)
            ApiKey.objects.get(user=store_user, api_key=api_key)
        except (StoreUser.DoesNotExist, ApiKey.DoesNotExist):
            is_auth = False
        else:
            is_auth = True
            context['store_user'] = store_user.to_dict()
    except KeyError:
        is_auth = False

    return is_auth, context
