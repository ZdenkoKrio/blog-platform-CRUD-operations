from django.views.generic import ListView
from ..models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'
    ordering = '-created_at'

    def get_queryset(self):
        queryset = Post.objects.all()

        # search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)

        # filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # order
        ordering = self.request.GET.get('ordering')
        if ordering == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_ordering'] = self.request.GET.get('ordering', 'newest')
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        return context
