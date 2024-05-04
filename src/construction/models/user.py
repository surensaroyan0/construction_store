from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class StoreUser(models.Model):
    GENDER_CHOICES = [
        (1, "Male"),
        (2, "Female")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile", null=True, blank=True)
    shipping_address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, null=True)

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.user.first_name,
            "lastname": self.user.last_name,
            "username": self.user.username,
            "email": self.user.email,
            "profile_picture": self.profile_picture,
            "shipping_address": self.shipping_address,
            "phone_number": self.phone_number,
            "gender": self.get_gender_display()
        }

    def __str__(self) -> str:
        return f"{self.user.username}"


@admin.register(StoreUser)
class StoreUserAdmin(admin.ModelAdmin):
    list_display = ["get_user_info", "shipping_address", "phone_number"]
    search_fields = ["get_user_info"]

    def get_user_info(self, obj):
        return obj.user.username
    get_user_info.short_description = "User"
