from catalog.models import Product


def get_products_by_category(category_id):
    """
    Возвращает список всех продуктов в указанной категории.

    :param category_id: ID категории
    :return: QuerySet продуктов
    """
    return Product.objects.filter(
        category_id=category_id
    ).select_related('category').order_by('-created_at')
