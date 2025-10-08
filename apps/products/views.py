from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Categorie, Produit, MouvementStock
from .serializers import CategorieSerializer, ProduitSerializer, MouvementStockSerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'categorie', 'actif']
    search_fields = ['code', 'nom']
    ordering_fields = ['code', 'nom', 'prix_unitaire_ht', 'quantite_stock']

    @action(detail=True, methods=['post'])
    def mouvement(self, request, pk=None):
        """Créer un mouvement de stock pour ce produit"""
        produit = self.get_object()
        serializer = MouvementStockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(produit=produit, cree_par=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MouvementStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MouvementStock.objects.all()
    serializer_class = MouvementStockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['produit', 'type_mouvement']