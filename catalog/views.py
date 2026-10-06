from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product
from catalog.forms import ContactForm, ProductForm


class HomeView(ListView):
    """Главная страница с каталогом товаров (доступна всем)"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    """Страница контактов с формой обратной связи (доступна всем)"""
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
            messages.success(request, 'Ваше сообщение успешно отправлено! Спасибо! ✅')
            form = ContactForm()
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме ⚠️')
        context['form'] = form
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    """Детальная страница товара (доступна всем)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# ========== CRUD для Product (только для авторизованных) ==========

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара (только для авторизованных)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')