from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Brand(models.Model):
    """برند محصولات الکترونیکی"""
    name = models.CharField(max_length=100, unique=True, verbose_name='نام برند')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='اسلاگ')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name='لوگو')
    country = models.CharField(max_length=50, blank=True, verbose_name='کشور سازنده')
    warranty_info = models.TextField(blank=True, verbose_name='اطلاعات گارانتی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('brand_detail', args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام برچسب')
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='اسلاگ')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='دسته‌بندی والد')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_products', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='دسته‌بندی')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='برند')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name='برچسب‌ها')
    name = models.CharField(max_length=200, verbose_name='نام محصول')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='اسلاگ')
    description = models.TextField(verbose_name='توضیحات')
    technical_description = models.TextField(blank=True, verbose_name='توضیحات فنی')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت (ریال)')
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name='قیمت با تخفیف (ریال)')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی')
    sku = models.CharField(max_length=50, blank=True, verbose_name='کد انبار')
    image = models.ImageField(upload_to='products/', verbose_name='تصویر اصلی')
    image_hover = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر هاور')
    warranty_period = models.CharField(max_length=100, blank=True, verbose_name='مدت گارانتی')
    weight = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True, verbose_name='وزن (گرم)')
    dimensions = models.CharField(max_length=100, blank=True, verbose_name='ابعاد')
    energy_label = models.CharField(max_length=10, blank=True, verbose_name='برچسب مصرف انرژی')
    is_original = models.BooleanField(default=True, verbose_name='کالای اصل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_featured = models.BooleanField(default=False, verbose_name='محصول ویژه')
    is_hot_deal = models.BooleanField(default=False, verbose_name='فروش ویژه')
    hot_deal_discount = models.PositiveIntegerField(default=0, blank=True, verbose_name='درصد تخفیف فروش ویژه')
    hot_deal_end = models.DateTimeField(blank=True, null=True, verbose_name='زمان پایان فروش ویژه')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='عنوان سئو')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='توضیحات متای سئو')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def total_stock(self):
        return self.stock

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


class Specification(models.Model):
    """مشخصات فنی محصولات الکترونیکی"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications', verbose_name='محصول')
    key = models.CharField(max_length=100, verbose_name='عنوان مشخصه')
    value = models.CharField(max_length=200, verbose_name='مقدار')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'مشخصات فنی'
        verbose_name_plural = 'مشخصات فنی'
        ordering = ['order']

    def __str__(self):
        return f'{self.key}: {self.value}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery', verbose_name='محصول')
    image = models.ImageField(upload_to='products/gallery/', verbose_name='تصویر')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'تصاویر گالری'
        ordering = ['order']

    def __str__(self):
        return f'تصویر {self.order} - {self.product.name}'




class Wishlist(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'علاقه‌مندی'
        verbose_name_plural = 'علاقه‌مندی‌ها'
        unique_together = ['user', 'product']

    def __str__(self):
        return f'{self.user} - {self.product.name}'