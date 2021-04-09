from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from django.conf import settings
import uuid

# Create your models here.

UserModel = get_user_model()


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


class Profile(models.Model):
    phone = models.CharField(max_length=10, default='')
    picture = models.ImageField(
        "Profile picture", upload_to="profile_pics/%Y-%m-%d/", null=True, blank=True
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    # READ-ONLY
    created = models.DateTimeField(auto_now_add=True, editable=False)

    # READ-ONLY
    updated = models.DateTimeField(auto_now=True, editable=False)
