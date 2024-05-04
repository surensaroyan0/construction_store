from django.db import models
from django.contrib import admin

from .user import StoreUser


class ApiKey(models.Model):
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=16)

    def __str__(self) -> str:
        return self.user.user.username
    

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ["id", "get_user_info", "api_key"]

    def get_user_info(self, obj):
        return obj.user.user.username
    get_user_info.short_description = "User"
