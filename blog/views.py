from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from blog.models import BlogPost
from blog.forms import BlogPostForm


class BlogPostListView(ListView):
    """Список опубликованных статей"""
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Фильтрация: только опубликованные
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница статьи с увеличением просмотров"""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Увеличиваем счётчик просмотров
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj


class BlogPostCreateView(CreateView):
    """Создание новой статьи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(UpdateView):
    """Редактирование статьи с редиректом на просмотр"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self):
        # Редирект на просмотр этой статьи
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление статьи"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')