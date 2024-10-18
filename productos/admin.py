from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group, Permission
from .models import Producto, Compra, Categoria
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

#Register your models here.


class CustomAdminSite(admin.AdminSite):

    def has_permission(self, request):
        
        if request.user.is_superuser:
            return True
        # Los usuarios del grupo 'clientes' tienen acceso al admin pero sin permisos de visualización
        elif request.user.groups.filter(name='clientes').exists():
            return request.user.is_staff
        
        return False

    def get_model_perms(self, request):
        """
        Limita los permisos para los usuarios que pertenecen al grupo 'clientes',
        haciéndolos invisibles en el admin.
        """
        if request.user.groups.filter(name='clientes').exists():
            return {}  
        
        return super().get_model_perms(request)


custom_admin_site = CustomAdminSite(name='admin')


@admin.register(Producto, site=custom_admin_site)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'fecha_creacion')
    list_filter = ('disponible', 'categoria', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('-fecha_creacion',)


@admin.register(Compra, site=custom_admin_site)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'total', 'fecha')
    list_filter = ('total', 'fecha')
    search_fields = ('cliente', 'total')
    ordering = ('-fecha',)


@admin.register(Categoria, site=custom_admin_site)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'nombre')
    search_fields = ('nombre', 'descripcion', 'fecha_creacion')
    ordering = ('-fecha_creacion',)


@admin.register(User, site=custom_admin_site) 
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Group, site=custom_admin_site) 
class GroupaAdmin(admin.ModelAdmin):
    pass

