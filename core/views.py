from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from products.models import Product
from blog.models import BlogPost
from core.models import NewsletterSubscriber


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_active=True, is_featured=True).select_related('brand')[:6]
        context['new_products'] = Product.objects.filter(is_active=True).select_related('brand').order_by('-created_at')[:8]
        context['hot_deals'] = Product.objects.filter(is_active=True, is_hot_deal=True).select_related('brand')[:4]
        context['special_offers'] = Product.objects.filter(is_active=True, discount_price__isnull=False).select_related('brand')[:6]
        context['latest_posts'] = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:5]
        return context


class AboutUsView(TemplateView):
    template_name = 'about-us.html'


class TermsConditionsView(TemplateView):
    template_name = 'terms-conditions.html'


class MyWishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'my-wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from products.models import Wishlist
        context['wishlist_items'] = Wishlist.objects.filter(user=self.request.user)
        return context


class ProductComparisonView(TemplateView):
    template_name = 'product-comparison.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compare_ids = self.request.session.get('compare_products', [])
        context['compare_products'] = Product.objects.filter(id__in=compare_ids, is_active=True).select_related('brand', 'category')
        return context


class NewsletterSubscribeView(View):
    def post(self, request):
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, 'ایمیل شما با موفقیت ثبت شد.')
        return redirect('home')


class AddToCompareView(View):
    def get(self, request, product_id):
        compare = request.session.get('compare_products', [])
        if product_id not in compare and len(compare) < 4:
            compare.append(product_id)
        request.session['compare_products'] = compare
        return redirect('product_comparison')


class RemoveFromCompareView(View):
    def get(self, request, product_id):
        compare = request.session.get('compare_products', [])
        if product_id in compare:
            compare.remove(product_id)
        request.session['compare_products'] = compare
        return redirect('product_comparison')