from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def __str__(self):
        return f'سبد خرید {self.user}'

    @property
    def total_price(self):
        return sum(item.total for item in self.items.all())

    @property
    def total_items(self):
        return self.items.count()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def total(self):
        return self.product.final_price * self.quantity