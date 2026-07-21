from django.contrib import admin
from .models import (
    FooterColumn, FooterLink, SiteSettings, ContactInfo, StaticPage,
    Slider, SidebarBanner, SidebarWidget,
    NavigationMenu, SiteBanner, SiteSection, NewsletterSubscriber
)


# ========== تنظیمات اصلی سایت ==========

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('اطلاعات فروشگاه', {
            'fields': ('site_name', 'logo', 'favicon', 'copyright_text')
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'phone', 'email')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('facebook', 'twitter', 'instagram', 'telegram')
        }),
        ('باکس‌های ویژگی', {
            'fields': (
                ('feature_1_icon', 'feature_1_text'),
                ('feature_2_icon', 'feature_2_text'),
                ('feature_3_icon', 'feature_3_text'),
                ('feature_4_icon', 'feature_4_text'),
            ),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('اطلاعات صفحه', {
            'fields': ('title', 'description')
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'phone', 'mobile', 'email')
        }),
        ('ساعات کاری', {
            'fields': ('working_hours_sat_wed', 'working_hours_thu', 'working_hours_fri')
        }),
        ('سئو', {
            'fields': ('meta_title', 'meta_description'),
        }),
    )

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['get_page_type_display', 'title', 'is_active', 'updated_at']
    list_filter = ['is_active']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('page_type', 'title', 'content', 'image', 'is_active')
        }),
        ('سئو', {
            'fields': ('meta_title', 'meta_description'),
        }),
    )


# ========== اسلایدر و بنرها ==========

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']


@admin.register(SidebarBanner)
class SidebarBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'order', 'is_active']
    list_filter = ['position', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(SidebarWidget)
class SidebarWidgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'order', 'is_active']
    list_filter = ['position', 'is_active']
    list_editable = ['order', 'is_active']


# ========== منوی ناوبری جدید ==========

@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type', 'category', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'page_type']
    list_editable = ['order', 'is_active']
    search_fields = ['title']


# ========== بنرهای سایت ==========

@admin.register(SiteBanner)
class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active']
    list_filter = ['is_active', 'position']
    fieldsets = (
        ('اطلاعات بنر', {
            'fields': ('title', 'image', 'link', 'description', 'position', 'is_active')
        }),
    )


# ========== عناوین بخش‌ها ==========

@admin.register(SiteSection)
class SiteSectionAdmin(admin.ModelAdmin):
    list_display = ['get_section_key_display', 'title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']


# ========== خبرنامه ==========

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active']
    search_fields = ['email']
    actions = ['make_inactive']

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = 'غیرفعال کردن مشترکین انتخاب شده'


# ========== فوتر ==========

class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ['title', 'url', 'order', 'is_active']


@admin.register(FooterColumn)
class FooterColumnAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    inlines = [FooterLinkInline]