from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View, TemplateView
from products.models import Product
from .models import Cart, CartItem


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'shopping-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        return self._add_to_cart(request, product_id)

    def get(self, request, product_id):
        return self._add_to_cart(request, product_id)

    def _add_to_cart(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.POST.get('quantity', request.GET.get('quantity', 1)))

        # Check inventory
        max_stock = product.stock
        if max_stock <= 0:
            messages.error(request, 'موجودی این محصول به پایان رسیده است.')
            return redirect('product_detail', slug=product.slug)

        # Find existing cart item
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > max_stock:
                messages.error(
                    request,
                    f'موجودی کافی نیست. موجودی فعلی: {max_stock} عدد. شما قبلاً {cart_item.quantity} عدد در سبد دارید.'
                )
                return redirect('product_detail', slug=product.slug)
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            if quantity > max_stock:
                messages.error(
                    request,
                    f'تعداد انتخابی ({quantity} عدد) بیشتر از موجودی ({max_stock} عدد) است.'
                )
                return redirect('product_detail', slug=product.slug)
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        messages.success(request, f'«{product.name}» به سبد خرید اضافه شد.')
        return redirect('cart_detail')


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'آیتم از سبد خرید حذف شد.')
        return redirect('cart_detail')