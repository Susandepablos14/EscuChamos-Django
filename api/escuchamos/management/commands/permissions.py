from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from escuchamos.models import Role

class Command(BaseCommand):
    help = 'Sembrar permisos a la base de datos'

    def handle(self, *args, **options):  
        self.seed_admin_permissions()
        self.seed_volunteer_permissions()
        self.seed_user_permissions()
        
    def seed_admin_permissions(self):
        admin_role = Role.objects.get(name='Administrador')

        all_permissions = Permission.objects.all()

        admin_role.permissions.add(*all_permissions)

    def seed_volunteer_permissions(self):
            volunteer_role = Role.objects.get(name='Voluntario')

            permissions_codenames = [
                
            ]

            permissions = Permission.objects.filter(codename__in=permissions_codenames)

            volunteer_role.permissions.add(*permissions)
    
    def seed_user_permissions(self):
            user_role = Role.objects.get(name='Usuario Normal')

            permissions_codenames = [
                
            ]

            permissions = Permission.objects.filter(codename__in=permissions_codenames)

            user_role.permissions.add(*permissions)