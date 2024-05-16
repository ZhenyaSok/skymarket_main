from django.core.management import BaseCommand
from ...models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='zhenyapaiton@yandex.ru',
            first_name='admin_main',
            last_name='custom',
            role='admin',
            is_active=True,
        )
        user.set_password('123456')
        user.save()