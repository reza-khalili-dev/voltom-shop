from django.contrib import admin
from .models import Brand, Category, Tag, Product, ProductImage, Specification, ProductInventory, Wishlist


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'order']


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1
    fields = ['key', 'value', 'order']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'country']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'discount_price', 'total_stock', 'is_active', 'is_featured', 'is_hot_deal']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active', 'is_featured', 'is_hot_deal', 'category', 'brand', 'tags']
    search_fields = ['name', 'description']
    filter_horizontal = ['tags']
    inlines = [ProductImageInline, SpecificationInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'category', 'brand', 'tags', 'description', 'technical_description')
        }),
        ('قیمت', {
            'fields': ('price', 'discount_price')
        }),
        ('تصاویر', {
            'fields': ('image',)
        }),
        ('مشخصات فنی', {
            'fields': ('warranty_period', 'weight', 'dimensions', 'energy_label', 'is_original')
        }),
        ('تنظیمات نمایش', {
            'fields': ('is_active', 'is_featured', 'is_hot_deal', 'hot_deal_discount', 'hot_deal_end')
        }),
        ('سئو', {
            'fields': ('meta_title', 'meta_description'),
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'image']


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'stock', 'sku', 'warehouse_location']
    search_fields = ['product__name', 'sku']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']