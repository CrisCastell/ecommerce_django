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
        self.productos_list_url = reverse('productos-list')
        self.productos_create_url = reverse('productos-list')
        self.productos_filtrar_productos_carrito = reverse('productos-filtrar-productos-carrito')


    def test_listar_productos_con_stock(self):

        self.client.login(username='cliente', password='password123')
        response = self.client.get(self.productos_list_url)

        # Productos con stock > 0 sean listados
        productos = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(productos), 2)  # (Producto 1 y 3)

        for producto in productos:
            self.assertGreater(producto['stock'], 0)

        
    def test_producto_inexistente(self):
        url = reverse('productos-detail', kwargs={'pk': 999})
        self.client.login(username='cliente', password='password123')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_validar_productos_carrito(self):
        # Agregar Producto 3 con cantidad mayor a su stock
        
        data1 = [
            {'producto_id': self.producto3.id, 'cantidad': 60}
        ]

        self.client.login(username='cliente', password='password123')  # Inicia sesión con un usuario cliente
        response = self.client.post(self.productos_filtrar_productos_carrito, data1, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Agregar Productos con cantidad correctas
        data2 = [
            
            {'producto_id': self.producto3.id, 'cantidad': 2, 'stock': 10},
            {'producto_id': self.producto1.id, 'cantidad': 3, 'stock': 5},
        ]

        response = self.client.post(self.productos_filtrar_productos_carrito, data2, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)



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

    def setUp(self):
        # Usuarios con roles distintos
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Compras por usuario
        self.compra1_user1 = Compra.objects.create(cliente=self.user1, total=100)
        self.compra2_user1 = Compra.objects.create(cliente=self.user1, total=150)
        
        self.compra1_user2 = Compra.objects.create(cliente=self.user2, total=200)

        # URL del endpoint para listar compras
        self.url_compras = reverse('compras-list')

    def test_usuario_solo_accede_a_su_historial(self):
        # Iniciar sesion
        self.client.login(username='user1', password='password123')

        #Visualiza sus compras
        response = self.client.get(self.url_compras)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        compras = response.json()
        
        self.assertEqual(len(compras), 2)


        for compra in compras:
            self.assertEqual(compra['cliente'], self.user1.username)

        self.client.logout()

        # Iniciar sesión como el segundo usuario y ver sus compras
        self.client.login(username='user2', password='password123')

        response = self.client.get(self.url_compras)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        compras = response.json()

        # Verifica que solo aparezca la compra del usuario2
        self.assertEqual(len(compras), 1)
        for compra in compras:
            self.assertEqual(compra['cliente'], self.user2.username)




    def test_usuario_no_puede_ver_detalle_de_otra_compra(self):
        # Iniciar sesion
        self.client.login(username='user1', password='password123')

        # Intentar ver detalle de la compra del user2
        url = reverse('compras-detail', kwargs={'pk': self.compra1_user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)