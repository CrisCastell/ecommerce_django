from django.db import models
from django.utils import timezone
import uuid
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)


    def __str__(self):
        return self.nombre

    @property
    def en_stock(self):
        return self.stock > 0
    


class Compra(models.Model):
    productos = models.ManyToManyField(Producto, through='CompraProducto')
    cliente = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    identificador_unico = models.CharField(max_length=8, unique=True, editable=False)  

    def __str__(self):
        return str(self.id)
    

    def save(self, *args, **kwargs):
        if not self.identificador_unico:
            self.identificador_unico = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Método para calcular el total de cada producto en la compra
    def total_producto(self):
        return self.cantidad * self.precio_unitario