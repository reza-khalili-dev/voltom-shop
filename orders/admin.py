from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem, Payment, ShippingMethod

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'sort_order']
    list_editable = ['price', 'is_active', 'sort_order']
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'shipping_method', 'shipping_cost', 'total_with_shipping', 'status', 'invoice_link', 'created_at']
    list_filter = ['status', 'shipping_method', 'created_at']
    search_fields = ['user__username', 'full_name', 'tracking_code']
    readonly_fields = ['total_price', 'total_with_shipping', 'shipping_cost', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
    mark_as_processing.short_description = 'تغییر وضعیت به در حال پردازش'

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'تغییر وضعیت به ارسال شده'

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'تغییر وضعیت به تحویل شده'

    def invoice_link(self, obj):
        url = reverse('download_invoice', args=[obj.id])
        return format_html(
            '<a href="{}" class="button" target="_blank">📄 دانلود فاکتور</a>',
            url
        )
    invoice_link.short_description = 'فاکتور'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'status', 'ref_id', 'created_at']
    list_filter = ['status']