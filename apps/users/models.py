from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('commercial', 'Commercial'),
        ('gestionnaire', 'Gestionnaire de stock'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='commercial')
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"