from django.contrib import admin
from django.db import models

from .user import StoreUser
from .product import Product


class Review(models.Model):
    RATING = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10')
    ]

    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING, null=True)
    comment = models.CharField(max_length=200, default="")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["rating", "date_posted"]
    # list_filter = ["get_user_info"]

    # def get_user_info(self, obj):
    #     return obj.user.user.username
    # get_user_info.short_description = "User"

    # def get_product_info(self, obj):
    #     return obj.product.name
    # get_product_info.short_description = "Product"
