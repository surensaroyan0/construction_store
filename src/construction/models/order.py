from django.contrib import admin
from django.db import models

from .user import StoreUser
from .product import Product


class Order(models.Model):
    STATUS_CHOICES = [
        (1, "Pending"),
        (2, "Processing"),
        (3, "Shipped"),
        (4, "Delivered"),
        (5, "Taken")
    ]

    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    product_price = models.PositiveIntegerField(default=1)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.user.username

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.user.username,
            "product": self.product,
            "quantity": self.quantity,
            "product_price": self.product_price,
            "status": self.get_status_display(),
            "date": self.order_date
        }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity", "product_price", "status", "order_date"]
    list_filter = ["status", "order_date"]
    search_fields = ["user__user__username", "product__name"]

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = "Status"
