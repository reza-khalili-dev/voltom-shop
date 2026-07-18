from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.views.static import serve
from .sitemap import StaticViewSitemap, ProductSitemap, CategorySitemap, BlogSitemap, BrandSitemap


admin.site.site_header = 'پنل مدیریت Voltom'
admin.site.site_title = 'Voltom'
admin.site.index_title = 'مدیریت فروشگاه لوازم برقی'

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog': BlogSitemap,
    'brands': BrandSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('blog/', include('blog.urls')),
    path('contact-us/', include('contacts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)