from django.contrib import admin
from django.db import models

from .category import Category


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category.name,
            "name": self.name
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    # list_filter = ["category_info"]

    # def category_info(self, obj):
    #     return obj.category.name
    # category_info.short_description = "Category"
