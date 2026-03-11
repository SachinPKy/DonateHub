from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

from .models import Donation, DonationImage, DonationTracking, DonationStatus, KERALA_DISTRICTS
from .forms import RegisterForm, DonationForm
from .utils.receipt_pdf import render_to_pdf


# ================= HOME =================
def home(request):
    return redirect(settings.FRONTEND_URL)


def register(request):
    return redirect(f"{settings.FRONTEND_URL}/register")


def social_login_cancelled(request):
    return redirect(f"{settings.FRONTEND_URL}/login?error=cancelled")


def social_login_error(request):
    return redirect(f"{settings.FRONTEND_URL}/login?error=auth_failed")


@login_required
def add_donation(request):
    return redirect(f"{settings.FRONTEND_URL}/add")


@login_required
def my_donations(request):
    return redirect(f"{settings.FRONTEND_URL}/my-donations")


# ================= AI CATEGORY =================
def ai_category(request):
    """AI-powered category suggestion based on description."""
    description = request.GET.get('description', '').lower()
    
    fallback = "Household Items"
    if not description:
        return JsonResponse({"category": fallback})
    
    if "book" in description:
        fallback = "Books"
    elif "toy" in description:
        fallback = "Toys"
    elif "laptop" in description or "mobile" in description:
        fallback = "Electronics"
    elif "shoe" in description:
        fallback = "Footwear"
    elif "shirt" in description or "pant" in description:
        fallback = "Clothes"
    elif "table" in description or "chair" in description:
        fallback = "Furniture"
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        prompt = (
            "Choose ONE category from this list ONLY:\n"
            "Clothes, Books, Toys, Electronics, Furniture, Footwear, "
            "Educational Materials, Household Items.\n\n"
            f"Description: {description}\n"
            "Return only the category name."
        )
        
        response = model.generate_content(prompt)
        ai_text = response.text.lower()
        
        categories = {
            "clothes": "Clothes",
            "books": "Books",
            "toys": "Toys",
            "electronics": "Electronics",
            "furniture": "Furniture",
            "footwear": "Footwear",
            "educational": "Educational Materials",
            "household": "Household Items",
        }
        
        for key, value in categories.items():
            if key in ai_text:
                return JsonResponse({"category": value})
    
    except Exception as e:
        logger.warning(f"Gemini AI failed: {e}")
    
    return JsonResponse({"category": fallback})


# ================= STATUS UPDATE =================
@login_required
def update_status(request, donation_id):
    """Update donation status (admin only)."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access required.")
    
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in DonationStatus.CHOICES]:
            donation.status = new_status
            donation.save()
            
            # Update tracking
            tracking, created = DonationTracking.objects.get_or_create(donation=donation)
            tracking.save()
            
            messages.success(request, f"Status updated to {new_status}")
    
    return redirect('admin_dashboard')


# ================= DONATION TRACKING =================
@login_required
def donation_tracking(request, donation_id):
    return redirect(f"{settings.FRONTEND_URL}/tracking/{donation_id}")


# ================= DOWNLOAD RECEIPT =================
@login_required
def download_receipt(request, donation_id):
    """Generate and download PDF receipt for donation."""
    donation = get_object_or_404(
        Donation.objects.prefetch_related('images', 'tracking'),
        id=donation_id
    )

    if donation.donor != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized.")
    
    # Get absolute URLs for images (xhtml2pdf needs full URLs)
    images = donation.images.all()
    image_urls = [request.build_absolute_uri(img.image.url) for img in images]
    
    html = render_to_string('receipt.html', {
        'donation': donation,
        'generated_date': timezone.now(),
        'image_urls': image_urls,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{donation.receipt_number}.pdf"'
    
    try:
        from xhtml2pdf import pisa
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            logger.error(f"PDF generation had errors: {pisa_status.err}")
            # Fallback to HTML
            response.write(html.encode('utf-8'))
            response['Content-Type'] = 'text/html'
            response['Content-Disposition'] = f'attachment; filename="receipt_{donation.receipt_number}.html"'
    except Exception as e:
        logger.error(f"PDF creation failed: {e}")
        response.write(html.encode('utf-8'))
        response['Content-Type'] = 'text/html'
        response['Content-Disposition'] = f'attachment; filename="receipt_{donation.receipt_number}.html"'

    return response


# ================= ADMIN DASHBOARD =================
@login_required
def admin_dashboard(request):
    return redirect(f"{settings.FRONTEND_URL}/admin")


# ================= API: GET DISTRICTS =================
def get_districts_json(request):
    """Return list of Kerala districts as JSON."""
    data = [{'id': name, 'name': name} for name, display in KERALA_DISTRICTS]
    return JsonResponse(data)


@login_required
def verify_otp(request, donation_id):
    return redirect(f"{settings.FRONTEND_URL}/verify-otp")
