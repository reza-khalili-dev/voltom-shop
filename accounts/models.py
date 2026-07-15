from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='شماره تماس')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    is_admin_user = models.BooleanField(default=False, verbose_name='ادمین فروشگاه')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.get_full_name() or self.username