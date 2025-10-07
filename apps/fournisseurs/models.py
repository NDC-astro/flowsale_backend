from django.db import models
from django.core.validators import RegexValidator
# Create your models here.


class Fournisseur(models.Model):
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
    produit_fourni = models.CharField(max_length=255, blank=True, null=True, help_text="Type de produit ou service fourni")
    date_ajout = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.raison_sociale

    class Meta:
        ordering = ['raison_sociale']
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"