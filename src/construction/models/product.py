from django.contrib import admin
from django.db import models
from django.db.models import JSONField

from .subcategory import Subcategory


class Product(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=1)
    quantity_available = models.PositiveIntegerField(default=1)
    specifications = JSONField(null=True, blank=True)
    image = models.ImageField(upload_to="product", null=True, blank=True)
    bought_count = models.IntegerField(default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'subcategory': self.subcategory.name,
            'name': self.name,
            'price': self.price,
            'quantity_available': self.quantity_available,
            'specifications': self.specifications if self.specifications else "",
            'image': self.image if self.image else None
        }

    def __str__(self):
        return self.name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "specifications"]
    search_fields = ["name", "subcategory__name"]
    list_filter = ["subcategory__name"]
