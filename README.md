# Django Store: E-commerce con Roles de Admin y Cliente

Esta aplicacion con **Django** maneja dos tipos de usuarios: **administradores** y **clientes**. Ambos usuarios pueden acceder al panel de administración de Django, pero con diferentes vistas y permisos.
El proyecto hace uso tanto de las vistas del admin de Django como del uso de endpoints hecho con Djando Rest Framework

## Tipos de Usuarios

### 1. Administradores 
- Los administradores tienen acceso completo al panel de administración de Django Store.
- Pueden gestionar todos los modelos, crear, editar, y eliminar registros.
- Tienen acceso a todas las funcionalidades del sistema.

### 2. Clientes
- Los usuarios **clientes** tienen acceso limitado al panel de administración de Django.
- Al ingresar, los clientes verán un **dashboard personalizado** con una interfaz limitada.
- No pueden ver, editar ni eliminar registros dentro del sistema, solo tienen acceso a interactuar con la tienda.

## Características Principales
- **Autenticación de usuarios**: Diferenciación clara entre administradores y clientes.
- **Panel de administración personalizado**: Los usuarios ven diferentes interfaces en función de su rol.
- **Gestión de compras**: Los clientes pueden realizar compras, y los administradores pueden ver y gestionar las compras realizadas por los clientes.

## Requisitos Previos
- **Docker**: Se debe tener instalado Docker para ejecutar el contenedor con solo un comando

## Explicacion de la tienda
- Para ingresar como usuario cliente se debe registrar desde la vista de registro, accesible en el login
- Una vez ingresado con un usuario cliente se visualizara el listado de articulos de la tienda.
- Se podra ver el detalle de cada producto de manera dinamica y tambien agregar y quitar elementos del carrito
- Para comprar hay que presionar el boton de carrito en la esquina superior izquierda de la lista y abrira un modal con el resumen del carrito
- Al presionar comprar, se ejecutara una peticion de la creacion de la compra al backend
- Al ser la compra exitosa se visualizara un mensaje indicandolo y mostrando el numero de compra
- Del lado izquierdo de la vista se vera el historial de compra del usuario


## Cómo Levantar el Proyecto

Para levantar el proyecto, simplemente ejecuta el siguiente comando desde el directorio raíz del proyecto:

```bash
docker-compose up
