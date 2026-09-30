from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from catalog.models import Product, Category
from catalog.forms import ContactForm


def home(request):
    """Главная страница с каталогом товаров"""
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    """Страница контактов с формой обратной связи"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо! ✅')
            form = ContactForm()
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме ⚠️')
    else:
        form = ContactForm()

    return render(request, 'catalog/contacts.html', {'form': form})


def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
