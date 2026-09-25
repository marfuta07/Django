from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from catalog.models import Product, Category


def home(request):
    """Главная страница с каталогом товаров"""
    products = Product.objects.select_related('category').all()
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    """Страница контактов с формой обратной связи"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and phone and message:
            print(f'Сообщение от {name} ({phone}): {message}')
            messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо! ✅')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля! ⚠️')

    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})