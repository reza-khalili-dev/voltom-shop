from django.db import models
from django.conf import settings
from products.models import Product


class ShippingMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام روش ارسال')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='هزینه ارسال (ریال)')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    sort_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'روش ارسال'
        verbose_name_plural = 'روش‌های ارسال'
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.name} - {self.price} ریال'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('cancelled', 'لغو شده'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس')
    province = models.CharField(max_length=50, verbose_name='استان')
    city = models.CharField(max_length=50, verbose_name='شهر')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    
    shipping_method = models.ForeignKey(
        ShippingMethod, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='روش ارسال'
    )
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='هزینه ارسال')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    total_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مبلغ کل')
    total_with_shipping = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='مبلغ قابل پرداخت')
    tracking_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='کد پیگیری')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']

    def __str__(self):
        return f'سفارش #{self.id} - {self.user}'

    def save(self, *args, **kwargs):
        if not self.total_with_shipping and self.total_price and self.shipping_cost:
            self.total_with_shipping = self.total_price + self.shipping_cost
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت واحد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def total(self):
        return self.price * self.quantity


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'در انتظار'),
        ('successful', 'موفق'),
        ('failed', 'ناموفق'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name='سفارش')
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='مبلغ')
    authority = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد Authority')
    ref_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد پیگیری')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'

    def __str__(self):
        return f'پرداخت {self.order.id} - {self.status}'