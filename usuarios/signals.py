from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_client_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='clientes')
    if created:
        group.permissions.clear() 