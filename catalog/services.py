from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """
    Возвращает список всех продуктов в указанной категории.
    Сначала проверяет кэш по ключу `category_{id}`, если пусто — грузит из БД.

    :param category_id: ID категории
    :return: список продуктов
    """
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        # Кэш пуст — загружаем из БД
        products = list(
            Product.objects.filter(category_id=category_id)
            .select_related('category')
            .order_by('-created_at')
        )
        cache.set(cache_key, products, 60 * 15)   # TTL 15 минут

    return products
