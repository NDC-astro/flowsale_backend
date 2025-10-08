from rest_framework import serializers
from .models import Categorie, Produit, MouvementStock

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description']

class ProduitSerializer(serializers.ModelSerializer):
    prix_ttc = serializers.ReadOnlyField()
    class Meta:
        model = Produit
        fields = '__all__'

class MouvementStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouvementStock
        fields = '__all__'
        read_only_fields = ['date_mouvement', 'cree_par']