from django.contrib import admin
from django.db import models

from .user import StoreUser
from .product import Product


class Cart(models.Model):
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.user.user.username


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "get_user_info", "get_product_info"]

    def get_user_info(self, obj):
        return obj.user.user.username
    get_user_info.short_description = "User"

    def get_product_info(self, obj):
        return obj.product.name
    get_product_info.short_description = "Product"
