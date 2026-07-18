from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from jdatetime import datetime as jdatetime
import os


class InvoiceGenerator:
    """Generate PDF invoice with full Persian support"""

    @staticmethod
    def reshape_text(text):
        """Convert Persian text for reportlab display"""
        if not text:
            return ""
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)

    @staticmethod
    def generate(order):
        """Generate PDF invoice file"""
        
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Vazir.ttf')
        if not os.path.exists(font_path):
            font_path = os.path.join(settings.STATIC_ROOT, 'fonts', 'Vazir.ttf')
        
        try:
            pdfmetrics.registerFont(TTFont('Vazir', font_path))
            use_font = True
        except:
            use_font = False

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        if use_font:
            c.setFont('Vazir', 12)
        else:
            c.setFont('Helvetica', 12)

        jalali_date = jdatetime.fromgregorian(datetime=order.created_at).strftime('%Y/%m/%d - %H:%M')

        # Header
        c.drawString(80*mm, height - 20*mm, InvoiceGenerator.reshape_text("فاکتور خرید"))
        c.drawString(70*mm, height - 30*mm, InvoiceGenerator.reshape_text("Voltom - فروشگاه اینترنتی لوازم برقی"))
        c.line(20*mm, height - 35*mm, 190*mm, height - 35*mm)

        # Order info
        y = height - 50*mm
        c.drawString(20*mm, y, InvoiceGenerator.reshape_text(f"شماره سفارش: #{order.id}"))
        c.drawString(20*mm, y - 10*mm, InvoiceGenerator.reshape_text(f"تاریخ ثبت: {jalali_date}"))
        c.drawString(20*mm, y - 20*mm, InvoiceGenerator.reshape_text(f"نام خریدار: {order.full_name}"))
        c.drawString(20*mm, y - 30*mm, InvoiceGenerator.reshape_text(f"شماره تماس: {order.phone}"))
        c.drawString(20*mm, y - 40*mm, InvoiceGenerator.reshape_text(f"آدرس: {order.address}"))
        c.drawString(20*mm, y - 50*mm, InvoiceGenerator.reshape_text(f"استان/شهر: {order.province} - {order.city}"))
        c.drawString(20*mm, y - 60*mm, InvoiceGenerator.reshape_text(f"کد پستی: {order.postal_code}"))
        c.drawString(20*mm, y - 70*mm, InvoiceGenerator.reshape_text(f"روش ارسال: {order.shipping_method.name if order.shipping_method else 'نامشخص'}"))
        c.drawString(20*mm, y - 80*mm, InvoiceGenerator.reshape_text(f"وضعیت: {order.get_status_display()}"))

        # Items table
        y = y - 100*mm
        c.line(20*mm, y, 190*mm, y)
        y -= 10*mm

        c.drawString(20*mm, y, InvoiceGenerator.reshape_text("ردیف"))
        c.drawString(55*mm, y, InvoiceGenerator.reshape_text("نام محصول"))
        c.drawString(130*mm, y, InvoiceGenerator.reshape_text("تعداد"))
        c.drawString(155*mm, y, InvoiceGenerator.reshape_text("قیمت واحد"))
        c.drawString(190*mm, y, InvoiceGenerator.reshape_text("جمع"))

        y -= 5*mm
        c.line(20*mm, y, 190*mm, y)
        y -= 10*mm

        for idx, item in enumerate(order.items.all(), 1):
            if y < 40*mm:
                c.showPage()
                if use_font:
                    c.setFont('Vazir', 12)
                else:
                    c.setFont('Helvetica', 12)
                y = height - 30*mm

            c.drawString(20*mm, y, str(idx))
            c.drawString(55*mm, y, InvoiceGenerator.reshape_text(item.product.name[:25]))
            c.drawString(130*mm, y, str(item.quantity))
            c.drawString(155*mm, y, f"{item.price:,.0f}")
            c.drawString(190*mm, y, f"{item.total:,.0f}")
            y -= 10*mm

        # Totals
        y -= 10*mm
        c.line(20*mm, y, 190*mm, y)
        y -= 10*mm

        c.drawString(120*mm, y, InvoiceGenerator.reshape_text(f"جمع کل اقلام: {order.total_price:,.0f} ریال"))
        y -= 10*mm
        c.drawString(120*mm, y, InvoiceGenerator.reshape_text(f"هزینه ارسال: {order.shipping_cost:,.0f} ریال"))
        y -= 10*mm
        c.drawString(120*mm, y, InvoiceGenerator.reshape_text(f"مبلغ قابل پرداخت: {order.total_with_shipping:,.0f} ریال"))

        # Footer
        c.line(20*mm, 30*mm, 190*mm, 30*mm)
        c.drawString(50*mm, 20*mm, InvoiceGenerator.reshape_text("این فاکتور به صورت خودکار توسط سیستم تولید شده است."))
        c.drawString(70*mm, 10*mm, InvoiceGenerator.reshape_text("Voltom - تمامی حقوق محفوظ است © ۱۴۰۵"))

        c.save()
        buffer.seek(0)
        return buffer.getvalue()


def download_invoice(request, order_id):
    from django.shortcuts import get_object_or_404
    from .models import Order

    order = get_object_or_404(Order, id=order_id)

    if request.user != order.user and not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('شما دسترسی به این فاکتور ندارید.')

    try:
        pdf_content = InvoiceGenerator.generate(order)
    except Exception as e:
        return HttpResponse(f'خطا در تولید فاکتور: {str(e)}', status=500)

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice-{order.id}.pdf"'
    return response