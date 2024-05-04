from django.contrib import admin
from django.db import models
from django.db.models import JSONField

from .subcategory import Subcategorie


class Product(models.Model):
    subcategory = models.ForeignKey(Subcategorie, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity_available = models.PositiveIntegerField()
    specifications = JSONField(null=True, blank=True)
    image = models.ImageField(upload_to="product", null=True, blank=True)
    bought_count = models.IntegerField(default=0)

    def to_dict(self):
        if not self.specifications:
            self.specifications = ''
        return {
            'id': self.id,
            'subcategory': self.subcategory,
            'name': self.name,
            'price': self.price,
            'quantity_available': self.quantity_available,
            'specifications': self.specifications,
            'image': self.image
        }

    def __str__(self):
        return self.name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "specifications"]
    search_fields = ["name"]
    # list_filter = ["subcategory_info"]
    #
    # def subcategory_info(self, obj):
    #     return obj.subcategory.name
    # subcategory_info.short_description = "Subcategory"
