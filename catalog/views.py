from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from catalog.models import Product, Category
from catalog.forms import ContactForm, ProductForm
from catalog.services import get_products_by_category


class HomeView(ListView):
    """Главная страница с низкоуровневым кэшированием списка"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Сначала проверяем кэш, если пусто — грузим из БД"""
        cache_key = 'home_products_list'
        products = cache.get(cache_key)

        if products is None:
            # Кэш пуст — загружаем из БД
            products = list(Product.objects.select_related('category').all())
            cache.set(cache_key, products, 60 * 15)   # 15 минут

        return products


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


@method_decorator(cache_page(60 * 5), name='dispatch')   # кэш на 5 минут
class ProductDetailView(DetailView):
    """Детальная страница товара с кэшированием на 5 минут"""
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
        """Автоматически привязываем владельца + сброс кэша"""
        form.instance.owner = self.request.user
        messages.success(self.request, 'Товар успешно создан! ✅')
        response = super().form_valid(form)
        cache.delete('home_products_list')   # ← сброс кэша списка
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара (владелец ИЛИ модератор)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        """Проверка: владелец ИЛИ модератор с правом change_product"""
        product = self.get_object()
        user = self.request.user

        if product.owner == user:
            return True
        if user.has_perm('catalog.change_product'):
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('У вас нет прав на редактирование этого товара!')
        return super().handle_no_permission()

    def form_valid(self, form):
        """Сброс кэша после сохранения"""
        response = super().form_valid(form)
        cache.delete('home_products_list')   # ← сброс кэша списка
        return response

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

        if product.owner == user:
            return True
        if user.has_perm('catalog.delete_product'):
            return True
        return False

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('У вас нет прав на удаление этого товара!')
        return super().handle_no_permission()

    def form_valid(self, form):
        """Сброс кэша после удаления"""
        response = super().form_valid(form)
        cache.delete('home_products_list')   # ← сброс кэша списка
        return response


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Отмена публикации (только модератор с правом can_unpublish_product)"""
    model = Product
    fields = []
    template_name = 'catalog/product_unpublish.html'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        """Только модератор с can_unpublish_product"""
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied('У вас нет прав на снятие с публикации!')
        return super().handle_no_permission()

    def form_valid(self, form):
        """Снимаем товар с публикации"""
        form.instance.is_published = False
        messages.success(
            self.request,
            f'Товар "{form.instance.name}" снят с публикации',
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class CategoryProductsView(ListView):
    """Список товаров в категории (с кэшированием через сервис category_{id})"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Используем сервисную функцию с кэшем category_{id}"""
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        """Добавляем категорию в контекст"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        try:
            context['category'] = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            context['category'] = None
        return context