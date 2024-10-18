from .viewsets import ProductoViewSet, CompraViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'compras', CompraViewSet)

urlpatterns = router.urls