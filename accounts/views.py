from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'sign-in.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'خوش آمدید {user.username}! ثبت‌نام با موفقیت انجام شد.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'لطفاً خطاهای فرم را اصلاح کنید.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signup_form'] = context.get('form')
        context['login_form'] = AuthenticationForm()
        return context


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'sign-in.html'
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, f'خوش آمدید {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'نام کاربری یا رمز عبور اشتباه است.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = context.get('form')
        context['signup_form'] = SignUpForm()
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'با موفقیت خارج شدید.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'my-account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from orders.models import Order
        context['user_orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return context