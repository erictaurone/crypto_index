from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.conf import settings
from PIL import Image
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_image = models.ImageField(upload_to='users/user_images/', default='users/images/default_avatar.jpeg')
    birthday = models.DateField(blank=True, null=True)
    social_security_number = models.CharField(max_length=9, blank=True, null=True)
    default_fiat_deposit = models.BooleanField(default=False)
    address = models.CharField(max_length=300, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username + ' ( ' + self.first_name + ' ' + self.last_name + ' )'

    def image_tag(self):
        if self.user_image:
            return mark_safe(
                '<img src="{user_image}" style="width: 45px; height: auto;"/>'.format(user_image=self.user_image.url)
            )
        else:
            return mark_safe(
                '<img src="{static_url}{base_avatar_url}" style="width: 45px; height: auto;"/>'.format(
                    static_url=settings.STATIC_URL, base_avatar_url='users/images/default_avatar.jpeg'
                )
            )

    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.user_image.path)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_image.path)
