from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все данные и загружает тестовые продукты'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Начинаем загрузку тестовых данных...')

        # Удаляем все существующие данные
        self.stdout.write('🗑️ Удаляем старые данные...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создаём категории
        categories_data = [
            {'name': 'Рассылки', 'description': 'Сервисы для email и SMS рассылок'},
            {'name': 'Телеграм боты', 'description': 'Боты для Telegram'},
            {'name': 'Веб-приложения', 'description': 'Веб-приложения на Django'},
            {'name': 'Микросервисы', 'description': 'Микросервисная архитектура'},
            {'name': 'Утилиты', 'description': 'Полезные утилиты для разработчиков'},
        ]

        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description']
            )
            categories[category.name] = category
            self.stdout.write(f'✅ Создана категория: {category.name}')

        # Создаём продукты
        products_data = [
            {
                'name': 'Удобный сервис рассылок',
                'description': 'Простой и мощный сервис для email и SMS рассылок.',
                'price': 140.00,
                'category_name': 'Рассылки'
            },
            {
                'name': 'Телеграм бот для бизнеса',
                'description': 'Полноценный бот для Telegram с поддержкой заказов.',
                'price': 250.00,
                'category_name': 'Телеграм боты'
            },
            {
                'name': 'Django CRM система',
                'description': 'Готовая CRM система на Django.',
                'price': 500.00,
                'category_name': 'Веб-приложения'
            },
            {
                'name': 'Микросервис аутентификации',
                'description': 'Готовый микросервис для аутентификации на JWT.',
                'price': 300.00,
                'category_name': 'Микросервисы'
            },
            {
                'name': 'Telegram бот для магазина',
                'description': 'Бот для интернет-магазина с корзиной и оплатой.',
                'price': 350.00,
                'category_name': 'Телеграм боты'
            },
            {
                'name': 'Плагин аналитики',
                'description': 'Плагин для сбора и отображения аналитики сайта.',
                'price': 100.00,
                'category_name': 'Утилиты'
            },
        ]

        for prod_data in products_data:
            category = categories.get(prod_data['category_name'])
            if category:
                product = Product.objects.create(
                    name=prod_data['name'],
                    description=prod_data['description'],
                    price=prod_data['price'],
                    category=category
                )
                self.stdout.write(f'✅ Создан товар: {product.name} (${product.price})')
            else:
                self.stdout.write(f'❌ Категория "{prod_data["category_name"]}" не найдена')

        self.stdout.write(self.style.SUCCESS('\n✨ Загрузка завершена!'))
        self.stdout.write(self.style.SUCCESS(f'📁 Всего категорий: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📦 Всего товаров: {Product.objects.count()}'))