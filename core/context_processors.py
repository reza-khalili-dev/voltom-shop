from core.models import SiteSettings, Slider, SidebarBanner, SidebarWidget, StaticPage, ContactInfo, NavigationMenu, SiteBanner, SiteSection
from products.models import Category, Tag, Brand
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


def navigation_menu(request):
    menu_items = NavigationMenu.objects.filter(is_active=True, parent=None).select_related('category')
    return {'navigation_menu': menu_items}


def site_banners(request):
    """بنرهای سایت - به صورت لیست برای استفاده ساده در template"""
    banners = SiteBanner.objects.filter(is_active=True)
    # هر بنر با اسم position در دسترسه
    result = {}
    for banner in banners:
        result[banner.position] = banner
    return {'site_banners': result}


def site_sections(request):
    """عناوین بخش‌ها - به صورت لیست برای استفاده ساده در template"""
    sections = SiteSection.objects.filter(is_active=True)
    result = {}
    for section in sections:
        result[section.section_key] = section
    return {'site_sections': result}


def all_brands(request):
    brands = Brand.objects.filter(is_active=True)
    return {'all_brands': brands}


def sidebar_context(request):
    from core.models import SidebarBanner, SidebarWidget
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
    contact = ContactInfo.objects.first()
    return {'contact_info': contact}


def footer_columns(request):
    from core.models import FooterColumn
    columns = FooterColumn.objects.filter(is_active=True).prefetch_related('links')
    return {'footer_columns': columns}