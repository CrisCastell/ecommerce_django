from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Producto, Compra, CompraProducto, Categoria
from django.contrib.auth.models import User
from django.utils.http import urlencode

class ProductoTests(TestCase):
    def setUp(self):


        # Usuarios con roles distintos
        self.client = APIClient()
        self.user_cliente = User.objects.create_user(username='cliente', password='password123')
        self.user_admin = User.objects.create_superuser(username='admin', password='password123')

        # Productos de prueba
        self.producto1 = Producto.objects.create(nombre='Producto 1', precio=10000.00, stock=5)
        self.producto2 = Producto.objects.create(nombre='Producto 2', precio=30000.00, stock=0)  # Sin stock
        self.producto3 = Producto.objects.create(nombre='Producto 3', precio=20000.00, stock=10)

        # Endpoints
        self.productos_url = reverse('productos')
        self.productos_create_url = reverse('productos-create')


    def test_listar_productos_con_stock(self):

        response = self.client.get(self.productos_url)

        # Productos con stock > 0 sean listados
        productos = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(productos), 2)  # (Producto 1 y 3)

        for producto in productos:
            self.assertGreater(producto['stock'], 0)

        
    def test_producto_inexistente(self):
        url = reverse('producto-detail', kwargs={'pk': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_validar_cantidad_carrito(self):
        # Agregar Producto 3 con cantidad mayor a su stock
        url = reverse('agregar-al-carrito')
        data = {
            'producto_id': self.producto3.id,
            'cantidad': 50
        }

        self.client.login(username='cliente', password='password123')  # Inicia sesión con un usuario cliente
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'Cantidad solicitada supera el stock disponible.')



    def test_solo_admins_pueden_crear_productos(self):
        # Intentar crear producto como cliente regular (sin permisos)
        data = {
            'nombre': 'Nuevo Producto',
            'precio': 35000.00,
            'stock': 10
        }

        # Cliente sin permisos
        self.client.login(username='cliente', password='password123')
        response = self.client.post(self.productos_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Debe devolver un 403

        # Administrador 
        self.client.login(username='admin', password='password123')
        response = self.client.post(self.productos_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # El administrador puede crear productos




class CompraTests(TestCase):

    def test_usuario_solo_accede_a_su_carrito(self):
        # Endpoint del carrito de un usuario
        url = reverse('carrito-usuario')

        # Loguearse como cliente 1
        self.client.login(username='cliente', password='password123')
        response = self.client.get(url)

        # Validar que el cliente pueda ver su propio carrito
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        carrito_cliente1 = response.json()

        # Intentar acceder al carrito como otro usuario
        self.client.login(username='admin', password='password123')
        response = self.client.get(url)

        # Validar que no puede acceder al carrito de otro usuario
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)