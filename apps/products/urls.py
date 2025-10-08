from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategorieViewSet, ProduitViewSet, MouvementStockViewSet

router = DefaultRouter()
router.register(r'categories', CategorieViewSet)
router.register(r'produits', ProduitViewSet)
router.register(r'mouvements-stock', MouvementStockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]