from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Try(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selfie = models.ImageField(upload_to="selfie")
    outfit = models.ImageField(upload_to="outfit")

    def __str__(self):
        try_on = {
            "user_email": self.user.email,
            "selfie": self.selfie.name,
            "outfit": self.outfit.name,
        }
        return f"{try_on}"
