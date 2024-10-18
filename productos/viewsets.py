from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ProductoDetailSerializer, ProductoListSerializer, ProductoCarritoSerializer, CompraListSerializer, CompraCreateSerializer
from .models import Producto, Compra
from .permissions import IsClienteOStaff
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(stock__gt=0)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductoDetailSerializer

        return ProductoListSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'filtrar_productos_carrito']:
            return [IsAuthenticated(), IsClienteOStaff()]
        else:
            return [IsAdminUser()]

    
    @action(detail=False, methods=['post'], url_path='filtrar-productos-carrito')
    def filtrar_productos_carrito(self, request):
        
        articulos = request.data
        print(articulos)

        if not articulos:
            return Response({'error': 'El carrito está vacío.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductoCarritoSerializer(data=articulos, many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated(), IsClienteOStaff()]
        else:
            return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Compra.objects.all().order_by('-fecha')
        return Compra.objects.filter(cliente=user).order_by('-fecha')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CompraCreateSerializer
        return CompraListSerializer
