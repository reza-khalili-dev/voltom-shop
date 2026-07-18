from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product, Category, Brand
from blog.models import BlogPost


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ['home', 'about_us', 'contact_us', 'terms_conditions']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True)


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)


class BrandSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Brand.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()