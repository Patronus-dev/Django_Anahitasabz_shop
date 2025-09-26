from django.views.generic import ListView, DetailView
from .models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')

        if paginator and page_obj:
            start = max(page_obj.number - 2, 1)
            end = min(page_obj.number + 2, paginator.num_pages)
            context['page_range_limited'] = range(start, end + 1)

        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_blogs'] = Blog.objects.all().order_by('-id')
        context['latest_blogs'] = Blog.objects.all().order_by('-id')[:3]
        return context
