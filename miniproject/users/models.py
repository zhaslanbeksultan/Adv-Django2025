import pdfkit
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True, default='')
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('trader', 'Trader'),
        ('sales', 'Sales Representative'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.profile_picture:
            from PIL import Image
            img = Image.open(self.profile_picture)
            img.save(self.profile_picture.path)
        super().save(*args, **kwargs)

    def generate_pdf(self):
        html = render_to_string('users/profile_pdf.html', {'profile': self})
        pdf = pdfkit.from_string(html, False)
        return pdf