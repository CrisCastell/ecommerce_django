from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Crear el grupo 'clientes' con permisos limitados
def create_client_group():
    group, created = Group.objects.get_or_create(name='clientes')

    for model in ContentType.objects.all():
        view_perm = Permission.objects.filter(content_type=model, codename__startswith='view_')
        group.permissions.add(*view_perm)


create_client_group()