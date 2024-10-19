from rest_framework import serializers
from .models import Producto, Compra, CompraProducto
from django.db import transaction
from decimal import Decimal


class ProductoListSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.CharField(source='categoria.nombre', read_only=True)
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'imagen', 'nombre_categoria', 'stock']


class ProductoDetailSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.CharField(source='categoria.nombre', read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'


class ProductoCarritoSerializer(serializers.ModelSerializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

    class Meta:
        model = Producto
        fields = ['producto_id', 'cantidad']

    def validate(self, data):
        try:
            producto = Producto.objects.get(id=data['producto_id'])
        except Producto.DoesNotExist:
            raise serializers.ValidationError(f"Producto con ID {data['producto_id']} no existe.", 400)

        
        if data['cantidad'] <= 0:
            raise serializers.ValidationError({"error": "La cantidad debe ser mayor que 0."}, code=400)
        
        if data['cantidad'] > producto.stock:
            raise serializers.ValidationError({"error": "Cantidad solicitada supera el stock disponible."}, code=400)

        return data
    
    def get_imagen(self, obj):

        if obj.imagen:
            try:
                return obj.imagen.url
            except ValueError:
                return None
        return None 

    def to_representation(self, instance):
        producto = Producto.objects.get(id=instance['producto_id'])

        total_producto = producto.precio * instance['cantidad']
        imagen = self.get_imagen(producto)

        return {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio_unitario': producto.precio,
            'imagen': imagen,
            'cantidad': instance['cantidad'],
            'total': total_producto
        }



class CompraListSerializer(serializers.ModelSerializer):

    fecha = serializers.DateTimeField(format="%d %B, %Y %H:%M:%S")
    productos = ProductoListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Compra
        fields = '__all__'



    
class ArticuloSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)

    

class CompraCreateSerializer(serializers.ModelSerializer):

    articulos = ArticuloSerializer(many=True)

    class Meta:
        model = Compra
        fields = ['articulos']

    
    def validate_producto_id(self, value):
        if not Producto.objects.filter(id=value).exists():
            raise serializers.ValidationError("Producto no encontrado.")
        return value


    @transaction.atomic
    def create(self, validated_data):

        cliente = self.context['request'].user.username  
        articulos_data = validated_data.pop('articulos')
        total_compra = Decimal('0.00')

        compra = Compra.objects.create(cliente=cliente, total=0)


        for articulo_data in articulos_data:
            producto = Producto.objects.get(id=articulo_data['producto_id'])
            cantidad = articulo_data['cantidad']
            precio_unitario = producto.precio
            total_producto = precio_unitario * cantidad

        
            CompraProducto.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )

      
            producto.stock -= cantidad
            producto.disponible = producto.stock > 0
            producto.save()

            total_compra += total_producto


        compra.total = total_compra
        compra.save()

        return compra
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "total": instance.total,
            "fecha": instance.fecha,
            "identificador_unico": instance.identificador_unico
        }