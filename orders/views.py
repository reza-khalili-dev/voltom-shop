import logging
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View, TemplateView
from django.urls import reverse
from django.conf import settings
from cart.models import Cart
from .models import Order, OrderItem, Payment, ShippingMethod
from .services import ZarinpalService
from products.models import Product

logger = logging.getLogger(__name__)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user=self.request.user).first()
        context['cart'] = cart
        context['shipping_methods'] = ShippingMethod.objects.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.error(request, 'سبد خرید شما خالی است.')
            return redirect('cart_detail')

        shipping_method_id = request.POST.get('shipping_method')
        shipping_method = None
        shipping_cost = 0
        
        if shipping_method_id:
            try:
                shipping_method = ShippingMethod.objects.get(id=shipping_method_id, is_active=True)
                shipping_cost = shipping_method.price
            except ShippingMethod.DoesNotExist:
                messages.error(request, 'روش ارسال نامعتبر است.')
                return redirect('checkout')
        else:
            messages.error(request, 'لطفاً روش ارسال را انتخاب کنید.')
            return redirect('checkout')

        total_price = cart.total_price
        total_with_shipping = total_price + shipping_cost

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name', request.user.get_full_name()),
            phone=request.POST.get('phone', request.user.phone or ''),
            address=request.POST.get('address', request.user.address or ''),
            province=request.POST.get('province', ''),
            city=request.POST.get('city', ''),
            postal_code=request.POST.get('postal_code', ''),
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
            total_price=total_price,
            total_with_shipping=total_with_shipping,
            status='pending',
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.final_price,
            )

        zarinpal = ZarinpalService(
            merchant_id=settings.ZARINPAL_MERCHANT_ID, 
            sandbox=settings.ZARINPAL_SANDBOX
        )
        callback_url = request.build_absolute_uri(reverse('verify_payment'))

        result = zarinpal.create_payment(
            order_id=order.id,
            amount=total_with_shipping,
            callback_url=callback_url,
            description=f'سفارش شماره {order.id}',
        )

        if result.get('data') and result['data'].get('authority'):
            Payment.objects.create(
                order=order,
                amount=total_with_shipping,
                authority=result['data']['authority'],
                status='pending',
            )
            if settings.ZARINPAL_SANDBOX:
                return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{result["data"]["authority"]}')
            else:
                return redirect(f'https://www.zarinpal.com/pg/StartPay/{result["data"]["authority"]}')
        else:
            error_msg = result.get('errors', {}).get('message', 'خطای ناشناخته')
            logger.error(f'Zarinpal payment creation failed: {result}')
            messages.error(request, f'خطا در اتصال به درگاه پرداخت. {error_msg}')
            return redirect('checkout')


class VerifyPaymentView(LoginRequiredMixin, View):
    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        if not authority:
            messages.error(request, 'اطلاعات پرداخت ناقص است.')
            return redirect('checkout')

        try:
            payment = Payment.objects.select_related('order').get(authority=authority)
            order = payment.order

            if order.user != request.user:
                messages.error(request, 'دسترسی غیرمجاز.')
                return redirect('home')

            if payment.status == 'successful':
                messages.info(request, 'این پرداخت قبلاً تأیید شده است.')
                return redirect('order_history')

            if status == 'OK':
                zarinpal = ZarinpalService(
                    merchant_id=settings.ZARINPAL_MERCHANT_ID, 
                    sandbox=settings.ZARINPAL_SANDBOX
                )
                verify_result = zarinpal.verify_payment(
                    authority=authority, 
                    amount=order.total_with_shipping
                )

                if verify_result.get('data') and verify_result['data'].get('code') == 100:
                    payment.status = 'successful'
                    payment.ref_id = str(verify_result['data'].get('ref_id', ''))
                    payment.save()

                    order.status = 'paid'
                    order.tracking_code = str(verify_result['data'].get('ref_id', order.id))
                    order.save()

                    # Reduce stock after successful payment
                    for item in order.items.all():
                        product = item.product
                        if hasattr(product, 'inventory'):
                            product.inventory.stock = max(0, product.inventory.stock - item.quantity)
                            product.inventory.save()

                    # Clear cart
                    Cart.objects.filter(user=request.user).delete()

                    messages.success(
                        request, 
                        f'✅ پرداخت موفق! شماره سفارش: #{order.id} | کد پیگیری: {order.tracking_code}'
                    )
                    return redirect('order_history')
                else:
                    payment.status = 'failed'
                    payment.save()
                    order.status = 'cancelled'
                    order.save()
                    messages.error(request, 'خطا در تأیید پرداخت.')
            else:
                payment.status = 'failed'
                payment.save()
                order.status = 'cancelled'
                order.save()
                messages.warning(request, 'پرداخت توسط کاربر لغو شد.')

        except Payment.DoesNotExist:
            messages.error(request, 'اطلاعات پرداخت یافت نشد.')
        except Exception as e:
            logger.error(f'Payment verification error: {str(e)}')
            messages.error(request, 'خطای سیستمی. لطفاً با پشتیبانی تماس بگیرید.')

        return redirect('order_history')


class TrackOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'track-orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = None
        order_id = self.request.GET.get('order_id')
        if order_id:
            order = Order.objects.filter(id=order_id, user=self.request.user).first()
            if not order:
                messages.warning(self.request, 'سفارشی با این مشخصات یافت نشد.')
        context['order'] = order
        return context


class OrderHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'track-orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items__product').order_by('-created_at')
        
        from jdatetime import datetime as jdatetime
        for order in orders:
            order.jalali_date = jdatetime.fromgregorian(datetime=order.created_at).strftime('%Y/%m/%d')
        
        context['orders'] = orders
        return context