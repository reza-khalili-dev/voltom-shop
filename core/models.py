from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Voltom', verbose_name='نام سایت')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره تماس')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='لوگو')
    copyright_text = models.CharField(max_length=200, default='تمامی حقوق محفوظ است', verbose_name='متن کپی‌رایت')
    facebook = models.URLField(blank=True, null=True, verbose_name='فیس‌بوک')
    twitter = models.URLField(blank=True, null=True, verbose_name='توییتر')
    instagram = models.URLField(blank=True, null=True, verbose_name='اینستاگرام')
    telegram = models.URLField(blank=True, null=True, verbose_name='تلگرام')
    feature_1_icon = models.CharField(max_length=50, default='icon-truck', verbose_name='آیکون ویژگی ۱')
    feature_1_text = models.CharField(max_length=100, default='ارسال سریع به سراسر ایران', verbose_name='متن ویژگی ۱')
    feature_2_icon = models.CharField(max_length=50, default='icon-support', verbose_name='آیکون ویژگی ۲')
    feature_2_text = models.CharField(max_length=100, default='ضمانت اصالت کالا', verbose_name='متن ویژگی ۲')
    feature_3_icon = models.CharField(max_length=50, default='icon-money', verbose_name='آیکون ویژگی ۳')
    feature_3_text = models.CharField(max_length=100, default='پشتیبانی تخصصی', verbose_name='متن ویژگی ۳')
    feature_4_icon = models.CharField(max_length=50, default='icon-return', verbose_name='آیکون ویژگی ۴')
    feature_4_text = models.CharField(max_length=100, default='گارانتی معتبر', verbose_name='متن ویژگی ۴')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name='Favicon')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


class Slider(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name='عنوان')
    subtitle = models.CharField(max_length=200, blank=True, verbose_name='زیرعنوان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='sliders/', verbose_name='تصویر')
    link = models.URLField(blank=True, verbose_name='لینک')
    button_text = models.CharField(max_length=50, blank=True, default='همین حالا خرید کنید', verbose_name='متن دکمه')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'
        ordering = ['order']

    def __str__(self):
        return self.title or f'اسلایدر {self.id}'


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مشترک خبرنامه'
        verbose_name_plural = 'مشترکین خبرنامه'

    def __str__(self):
        return self.email


class NavigationMenu(models.Model):
    """منوی اصلی سایت - قابل کنترل کامل از پنل ادمین"""
    PAGE_TYPES = [
        ('home', 'صفحه اصلی'),
        ('blog', 'وبلاگ'),
        ('about', 'درباره ما'),
        ('contact', 'تماس با ما'),
        ('products', 'همه محصولات'),
        ('terms', 'قوانین و شرایط'),
        ('comparison', 'مقایسه محصولات'),
        ('track', 'پیگیری سفارش'),
        ('custom', 'لینک دلخواه'),
    ]

    title = models.CharField(max_length=100, verbose_name='عنوان منو')
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, default='custom', verbose_name='نوع صفحه')
    category = models.ForeignKey('products.Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته‌بندی')
    custom_url = models.CharField(max_length=200, blank=True, verbose_name='لینک دلخواه')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='زیرمنوی والد')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'منوی ناوبری'
        verbose_name_plural = 'منوهای ناوبری'
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.page_type == 'custom' and self.custom_url:
            return self.custom_url
        elif self.category:
            return self.category.get_absolute_url()
        else:
            urls = {
                'home': '/',
                'blog': '/blog/',
                'about': '/about-us/',
                'contact': '/contact-us/',
                'products': '/products/',
                'terms': '/terms-conditions/',
                'comparison': '/product-comparison/',
                'track': '/orders/track/',
            }
            return urls.get(self.page_type, '#')


class SiteBanner(models.Model):
    """بنرهای تبلیغاتی قابل کنترل از پنل ادمین"""
    POSITIONS = [
        ('home_wide_1', 'صفحه اصلی - بنر عریض ۱'),
        ('home_wide_2', 'صفحه اصلی - بنر عریض ۲'),
        ('home_wide_3', 'صفحه اصلی - بنر عریض ۳'),
        ('home_wide_4', 'صفحه اصلی - بنر عریض ۴'),
        ('home_wide_big', 'صفحه اصلی - بنر بزرگ'),
        ('sidebar_blog', 'سایدبار وبلاگ'),
        ('sidebar_category', 'سایدبار دسته‌بندی'),
        ('sidebar_detail', 'سایدبار جزئیات محصول'),
    ]

    title = models.CharField(max_length=100, verbose_name='عنوان بنر')
    image = models.ImageField(upload_to='banners/', verbose_name='تصویر بنر')
    link = models.URLField(blank=True, verbose_name='لینک بنر')
    position = models.CharField(max_length=20, choices=POSITIONS, unique=True, verbose_name='موقعیت نمایش')
    description = models.CharField(max_length=200, blank=True, verbose_name='متن روی بنر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'بنر سایت'
        verbose_name_plural = 'بنرهای سایت'
        ordering = ['position']

    def __str__(self):
        return f'{self.get_position_display()} - {self.title}'


class SiteSection(models.Model):
    """عناوین و متون قابل ویرایش بخش‌های مختلف سایت"""
    SECTION_KEYS = [
        ('hot_deals_title', 'عنوان بخش فروش ویژه'),
        ('special_offer_title', 'عنوان بخش پیشنهاد ویژه'),
        ('product_tags_title', 'عنوان بخش برچسب‌های محصول'),
        ('special_deals_title', 'عنوان بخش تخفیف‌های ویژه'),
        ('newsletter_title', 'عنوان بخش خبرنامه'),
        ('newsletter_desc', 'توضیحات خبرنامه'),
        ('new_products_title', 'عنوان بخش محصولات جدید'),
        ('featured_products_title', 'عنوان بخش محصولات ویژه'),
        ('featured_category_title', 'عنوان بخش لوازم برقی و الکترونیک'),
        ('latest_blog_title', 'عنوان بخش آخرین مقالات'),
        ('brands_title', 'عنوان بخش برندها'),
        ('promo_text', 'متن تخفیف نوار منو'),
    ]

    section_key = models.CharField(max_length=50, choices=SECTION_KEYS, unique=True, verbose_name='کلید بخش')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='زیرعنوان')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'عنوان بخش'
        verbose_name_plural = 'عناوین بخش‌ها'

    def __str__(self):
        return f'{self.get_section_key_display()}: {self.title}'


class SidebarBanner(models.Model):
    POSITIONS = [
        ('blog', 'وبلاگ'),
        ('category', 'دسته‌بندی'),
        ('detail', 'جزئیات محصول'),
    ]
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='banners/', verbose_name='تصویر')
    link = models.URLField(blank=True, verbose_name='لینک')
    position = models.CharField(max_length=50, choices=POSITIONS, verbose_name='موقعیت نمایش')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'بنر سایدبار'
        verbose_name_plural = 'بنرهای سایدبار'
        ordering = ['order']

    def __str__(self):
        return f'{self.title} - {self.position}'


class SidebarWidget(models.Model):
    POSITIONS = [
        ('blog', 'وبلاگ'),
        ('category', 'دسته‌بندی'),
        ('detail', 'جزئیات محصول'),
    ]
    title = models.CharField(max_length=100, verbose_name='عنوان ویجت')
    position = models.CharField(max_length=50, choices=POSITIONS, verbose_name='موقعیت')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'ویجت سایدبار'
        verbose_name_plural = 'ویجت‌های سایدبار'
        ordering = ['position', 'order']

    def __str__(self):
        return f'{self.title} - {self.position}'


class StaticPage(models.Model):
    PAGE_TYPES = [
        ('about', 'درباره ما'),
        ('terms', 'قوانین و شرایط'),
    ]
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, unique=True, verbose_name='نوع صفحه')
    title = models.CharField(max_length=200, verbose_name='عنوان صفحه')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='عنوان سئو')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='توضیحات متای سئو')
    content = models.TextField(verbose_name='متن اصلی')
    image = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name='تصویر اصلی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'صفحه استاتیک'
        verbose_name_plural = 'صفحات استاتیک'

    def __str__(self):
        return self.get_page_type_display()


class ContactInfo(models.Model):
    title = models.CharField(max_length=100, default='تماس با ما', verbose_name='عنوان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    address = models.TextField(verbose_name='آدرس')
    phone = models.CharField(max_length=20, verbose_name='تلفن')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='موبایل')
    email = models.EmailField(verbose_name='ایمیل')
    working_hours_sat_wed = models.CharField(max_length=50, blank=True, verbose_name='شنبه تا چهارشنبه')
    working_hours_thu = models.CharField(max_length=50, blank=True, verbose_name='پنجشنبه')
    working_hours_fri = models.CharField(max_length=50, default='تعطیل', verbose_name='جمعه')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='عنوان سئو')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='توضیحات متای سئو')

    class Meta:
        verbose_name = 'اطلاعات تماس'
        verbose_name_plural = 'اطلاعات تماس'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FooterColumn(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان ستون')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'ستون فوتر'
        verbose_name_plural = 'ستون‌های فوتر'
        ordering = ['order']

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    column = models.ForeignKey(FooterColumn, on_delete=models.CASCADE, related_name='links', verbose_name='ستون')
    title = models.CharField(max_length=100, verbose_name='عنوان لینک')
    url = models.CharField(max_length=200, verbose_name='آدرس', help_text='مثال: /about-us/ یا https://example.com')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک‌های فوتر'
        ordering = ['column', 'order']

    def __str__(self):
        return f'{self.title} ({self.column.title})'