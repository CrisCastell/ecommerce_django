from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def add_user_to_client_group(sender, instance, created, **kwargs):
    # Si el usuario es nuevo y no es un superusuario, lo agregamos al grupo "clientes"
    if created and not instance.is_superuser:
        client_group, created = Group.objects.get_or_create(name='clientes')
        instance.groups.add(client_group)


@receiver(post_migrate)
def create_client_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='clientes')
    if created:
        group.permissions.clear()  # Limpiar permisos solo si el grupo fue creado