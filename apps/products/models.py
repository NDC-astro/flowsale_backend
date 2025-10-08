from django.db import models
from django.core.validators import MinValueValidator

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Produit(models.Model):
    TYPE_CHOICES = [
        ('produit', 'Produit physique'),
        ('service', 'Service'),
    ]

    code = models.CharField(max_length=50, unique=True, verbose_name="Code produit")
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='produit')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)  # en %
    quantite_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    seuil_alerte = models.IntegerField(default=5, validators=[MinValueValidator(0)], help_text="Quantité en dessous de laquelle une alerte est déclenchée")
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @property
    def prix_ttc(self):
        return float(self.prix_unitaire_ht * (1 + self.taux_tva / 100))

    class Meta:
        ordering = ['code']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"


class MouvementStock(models.Model):
    TYPE_MOUVEMENT = [
        ('entree', 'Entrée de stock'),
        ('sortie', 'Sortie de stock'),
        ('ajustement', 'Ajustement manuel'),
    ]

    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT)
    quantite = models.IntegerField(validators=[MinValueValidator(1)])
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True)
    cree_par = models.CharField(max_length=150)  # username

    def save(self, *args, **kwargs):
        # Mettre à jour le stock du produit
        if self.type_mouvement == 'entree':
            self.produit.quantite_stock += self.quantite
        elif self.type_mouvement == 'sortie':
            if self.quantite > self.produit.quantite_stock:
                raise ValueError("Quantité insuffisante en stock.")
            self.produit.quantite_stock -= self.quantite
        elif self.type_mouvement == 'ajustement':
            self.produit.quantite_stock = self.quantite  # remplace la valeur
        self.produit.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_mouvement_display()} - {self.quantite} x {self.produit.nom}"

    class Meta:
        ordering = ['-date_mouvement']
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"