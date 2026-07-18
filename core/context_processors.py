from core.models import SiteSettings, Slider, SidebarBanner, SidebarWidget, StaticPage, ContactInfo
from products.models import Category, Tag
from cart.models import Cart


def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'site_settings': settings}


def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return {'all_categories': categories}


def cart_context(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    return {'cart': cart}


def sliders(request):
    return {'sliders': Slider.objects.filter(is_active=True)}


def all_tags(request):
    return {'all_tags': Tag.objects.all()}


def sidebar_context(request):
    from core.models import SidebarBanner, SidebarWidget
    from products.models import Tag
    from blog.models import BlogCategory
    return {
        'sidebar_banners': SidebarBanner.objects.filter(is_active=True),
        'sidebar_widgets': SidebarWidget.objects.filter(is_active=True),
        'blog_categories': BlogCategory.objects.filter(is_active=True),
    }


def static_pages(request):
    from core.models import StaticPage
    about_page = StaticPage.objects.filter(page_type='about', is_active=True).first()
    terms_page = StaticPage.objects.filter(page_type='terms', is_active=True).first()
    return {
        'about_page': about_page,
        'terms_page': terms_page,
    }


def contact_info(request):
    from core.models import ContactInfo
    contact = ContactInfo.objects.first()
    return {'contact_info': contact}


def footer_columns(request):
    from core.models import FooterColumn
    columns = FooterColumn.objects.filter(is_active=True).prefetch_related('links')
    return {'footer_columns': columns}