from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from .user import StoreUser


class Card(models.Model):
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=19)
    cardholder_name = models.CharField(max_length=255)
    expiration_month = models.CharField(max_length=2)
    expiration_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment Card - {self.card_number}"

    def masked_card_number(self):
        return f"**** **** **** {self.card_number[-4:]}"

    def to_dict(self):
        return {
            "id": self.id,
            "card_number": self.masked_card_number(),
            "cardholder_name": self.cardholder_name,
            "expiration_month": self.expiration_month,
            "expiration_year": self.expiration_year,
            "cvv": self.cvv,
            "is_main": self.is_main,
        }


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ["get_user", "card_number", "is_main"]
    search_fields = ["get_user"]

    def get_user(self, obj):
        return obj.user.user.username
    get_user.short_description = "User"
