from django.db import models
from django.core.validators import RegexValidator

class Client(models.Model):
    STATUT_CHOICES = [
        ('prospect', 'Prospect'),
        ('client', 'Client'),
        ('inactif', 'Inactif'),
    ]

    raison_sociale = models.CharField(max_length=255, verbose_name="Raison sociale")
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    pays = models.CharField(max_length=100, default="France")
    telephone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True,
        null=True
    )
    email = models.EmailField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='prospect')
    date_creation = models.DateTimeField(auto_now_add=True)
    derniere_interaction = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.raison_sociale

    class Meta:
        ordering = ['raison_sociale']
        verbose_name = "Client"
        verbose_name_plural = "Clients"
