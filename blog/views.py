from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Blog


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_blogs'] = Blog.objects.all().order_by('-id')
        context['latest_blogs'] = Blog.objects.all().order_by('-id')[:3][::-1]
        return context


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog': blog})

#
# @login_required(login_url='/accounts/login/')  # مسیر صفحه لاگین خودت را وارد کن
# def blog_like(request, pk):
#     blog = get_object_or_404(Blog, pk=pk)
#
#     if request.user in blog.likes.all():
#         blog.likes.remove(request.user)  # اگر قبلا لایک کرده بود، آنلایک کن
#     else:
#         blog.likes.add(request.user)  # اگر لایک نکرده بود، لایک کن
#
#     return redirect(reverse('blog_detail', args=[pk]))
