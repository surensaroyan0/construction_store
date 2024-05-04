from django.contrib import admin
from django.db import models


class Categorie(models.Model):
    name = models.CharField(max_length=50)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __str__(self):
        return self.name


@admin.register(Categorie)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_filter = ["name"]
