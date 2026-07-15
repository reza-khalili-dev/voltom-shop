from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name='اسلاگ')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دسته‌بندی مقاله'
        verbose_name_plural = 'دسته‌بندی‌های مقاله'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog') + f'?category={self.slug}'


class BlogPost(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='دسته‌بندی')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='اسلاگ')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='تصویر')
    content = models.TextField(verbose_name='متن مقاله')
    summary = models.TextField(max_length=500, verbose_name='خلاصه')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='عنوان سئو')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='توضیحات متای سئو')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def approved_comments_count(self):
        return self.comments.filter(is_approved=True).count

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog_detail', args=[self.slug])


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='کامنت والد')
    content = models.TextField(verbose_name='متن کامنت')
    is_approved = models.BooleanField(default=False, verbose_name='تأیید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.post.title[:30]}'