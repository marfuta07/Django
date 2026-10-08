from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from catalog.models import Product
from catalog.forms import ContactForm, ProductForm


class HomeView(ListView):
    """Главная страница с каталогом товаров"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsView(TemplateView):
    """Страница контактов"""
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
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


# ========== CRUD для Product ==========

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Автоматически привязываем владельца"""
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно создан! ✅')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара (только владелец)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        """Проверка: только владелец может редактировать"""
        product = self.get_object()
        return product.owner == self.request.user

    def handle_no_permission(self):
        """Если не владелец — ошибка 403"""
        if self.request.user.is_authenticated:
            raise PermissionDenied('Вы не являетесь владельцем этого товара!')
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара (владелец ИЛИ модератор)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        """Владелец ИЛИ модератор с правом delete_product"""
        product = self.get_object()
        user = self.request.user

        # Владелец может удалять
        if product.owner == user:
            return True

        # Модератор с правом delete_product может удалять
        if user.has_perm('catalog.delete_product'):
            return True

        return False

    def handle_no_permission(self):
        """Если не владелец и не модератор — ошибка 403"""
        if self.request.user.is_authenticated:
            raise PermissionDenied('У вас нет прав на удаление этого товара!')
        return super().handle_no_permission()
class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Отмена публикации (только модератор с правом can_unpublish_product)"""
    model = Product
    fields = []  # ничего не редактируем
    template_name = 'catalog/product_unpublish.html'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        """Только модератор с can_unpublish_product"""
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def form_valid(self, form):
        """Меняем статус на False"""
        product = self.get_object()
        product.is_published = False
        product.save()
        messages.success(self.request, f'Товар "{product.name}" снят с публикации')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})