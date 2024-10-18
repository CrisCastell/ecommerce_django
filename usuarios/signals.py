from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def add_user_to_client_group(sender, instance, created, **kwargs):
    # Si el usuario es nuevo y no es un superusuario, lo agregamos al grupo "clientes"
    if created and not instance.is_superuser:
        client_group, created = Group.objects.get_or_create(name='clientes')
        instance.groups.add(client_group)
