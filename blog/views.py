from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.db.models import Count, Q
from .models import BlogCategory, BlogPost, BlogComment


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True)
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(content__icontains=q))
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = BlogPost.objects.filter(is_published=True).annotate(
            comment_count=Count('comments', filter=Q(comments__is_approved=True))
        ).order_by('-comment_count')[:3]
        context['recent_posts'] = BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3]
        context['blog_categories'] = BlogCategory.objects.filter(is_active=True)
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog-details.html'
    context_object_name = 'post'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True, parent=None)
        return context


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(BlogPost, id=post_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent = None
        if parent_id:
            parent = get_object_or_404(BlogComment, id=parent_id)
        if content:
            BlogComment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent=parent
            )
        return redirect('blog_detail', slug=post.slug)