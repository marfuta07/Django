from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с нужными правами'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Создаём группу "Модератор продуктов"...')

        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write('✅ Группа создана')
        else:
            self.stdout.write('ℹ️ Группа уже существует, обновляем права')

        # Получаем ContentType для Product
        content_type = ContentType.objects.get_for_model(Product)

        # Права:
        # 1. can_unpublish_product (кастомное)
        # 2. delete_product (встроенное)
        permissions = [
            Permission.objects.get(
                codename='can_unpublish_product',
                content_type=content_type
            ),
            Permission.objects.get(
                codename='delete_product',
                content_type=content_type
            ),
        ]

        # Назначаем права группе
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(
            f'\n✨ Группа "Модератор продуктов" настроена!'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'📋 Права: {", ".join(p.name for p in group.permissions.all())}'
        ))
