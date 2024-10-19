from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from productos.models import Producto
from django.contrib.auth import get_user_model


# Create your tests here.
class AdminAccessTests(TestCase):


    def setUp(self):
        # Crear un superusuario
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin', password='adminpassword', email='admin@test.com'
        )

        # Crear un usuario staff que pertenece al grupo "clientes" automaticamente
        self.staff_user = get_user_model().objects.create_user(
            username='staff', password='staffpassword', email='staff@test.com', is_staff=True
        )

        # Producto de prueba
        self.producto1 = Producto.objects.create(nombre='Producto 1', precio=10000.00, stock=5)
        
        # URL para el dashboard del admin
        self.admin_url = reverse('admin:index')  

        # URL para ver, editar y eliminar el modelo Productos
        self.producto_list_url = reverse('admin:productos_producto_changelist')  
        self.producto_change_url = reverse('admin:productos_producto_change', args=[self.producto1.pk]) 






    def test_superuser_tiene_accesos_admin(self):
        
        self.client.login(username='admin', password='adminpassword')

        # El superusuario puede acceder al panel de administración
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Administración de sitio")  


        # Verificar que el superusuario puede ver la lista de productos y editar uno de ellos

        response = self.client.get(self.producto_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    def test_user_clientes_no_tiene_acceso(self):
        
        self.client.login(username='staff', password='staffpassword')

        # El usuario staff debería poder acceder al panel de administración
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Django Store")

        # Verificar que el usuario no puede ver la lista de productos
        response = self.client.get(self.producto_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 




    def test_staff_user_has_custom_dashboard(self):
        # Iniciar sesión como el usuario staff (grupo clientes)
        self.client.login(username='staff', password='staffpassword')

        # Acceder al dashboard del admin
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que tiene un dashboard personalizado (asumiendo que hay contenido personalizado en el template)
        self.assertContains(response, "Django Store")
        self.assertNotContains(response, "App Models")