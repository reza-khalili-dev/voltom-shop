from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Brand, Category, Product, Wishlist


class ProductListView(ListView):
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category', 'brand')
        
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q) |
                Q(brand__name__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        
        category_name = self.request.GET.get('category')
        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name)
        
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        brand = self.request.GET.get('brand')
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['category_filter'] = self.request.GET.get('category', '')
        return context


class CategoryProductsView(ListView):
    model = Product
    template_name = 'category.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        return Product.objects.filter(category=self.category, is_active=True).select_related('brand')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category', 'brand', 'inventory').prefetch_related('specifications', 'gallery', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_deals'] = Product.objects.filter(is_active=True, is_hot_deal=True).select_related('brand')[:4]
        context['upsell_products'] = Product.objects.filter(
            category=self.object.category, is_active=True
        ).select_related('brand').exclude(id=self.object.id)[:6]
        return context


class BrandListView(ListView):
    model = Brand
    template_name = 'category.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.filter(is_active=True)


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'category.html'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(brand=self.object, is_active=True).select_related('category')
        return context


class AddToWishlistView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
        return redirect('my_wishlist')


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        return redirect('my_wishlist')