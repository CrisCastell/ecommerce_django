from .viewsets import ProductoViewSet, CompraViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'compras', CompraViewSet, basename='compras')

urlpatterns = router.urls