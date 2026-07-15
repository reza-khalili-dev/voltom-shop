from django.contrib import messages
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm


class ContactUsView(FormView):
    template_name = 'contact-us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_us')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد.')
        return super().form_valid(form)