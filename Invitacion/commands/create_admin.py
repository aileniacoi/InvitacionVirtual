from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Crea un superusuario desde variables de entorno'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME')
        email = os.getenv('ADMIN_EMAIL')
        password = os.getenv('ADMIN_PASSWORD')

        if username and password and email:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado con éxito.'))
            else:
                self.stdout.write(f'El usuario "{username}" ya existe.')
        else:
            self.stdout.write('Faltan variables de entorno para crear el admin.')