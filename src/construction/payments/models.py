from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import admin

from ..models.user import StoreUser


class UserPayment(models.Model):
    store_user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, default=1)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ["get_user_info", "payment_bool", "stripe_checkout_id"]

    def get_user_info(self, obj):
        return obj.store_user.user.username

    get_user_info.short_description = "User"


@receiver(post_save, sender=StoreUser)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(store_user=instance)