from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render
from catalog.models import Product
from catalog.forms import ContactForm


class HomeView(ListView):
    """Главная страница с каталогом товаров"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    """Страница контактов с формой обратной связи"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        context = self.get_context_data()
        if form.is_valid():
            form.save()
            from django.contrib import messages
            messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо! ✅')
            form = ContactForm()
        else:
            from django.contrib import messages
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме ⚠️')
        context['form'] = form
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'