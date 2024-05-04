from django.contrib import admin
from django.db import models

from ..payments.models import UserPayment
from .user import StoreUser


class Order(models.Model):
    STATUS = [
        (1, "Pending"),
        (2, "Processing"),
        (3, "Shipped"),
        (4, "Delivered")
    ]

    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(UserPayment, on_delete=models.CASCADE, default=1)
    total_amount = models.DecimalField(default=0.0, max_digits=7, decimal_places=2)
    status = models.PositiveIntegerField(choices=STATUS, null=True)
    shipped_address = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "total_amount", "status", "shipped_address", "order_date"]
    # list_filter = ["get_user_info"]

    # def get_user_info(self, obj):
    #     return obj.user.user.username
    # get_user_info.short_description = 'User'
