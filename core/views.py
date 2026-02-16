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
import os

logger = logging.getLogger(__name__)

from .models import Donation, DonationImage, DonationTracking, DonationStatus, KERALA_DISTRICTS
from .forms import RegisterForm, DonationForm
from .utils.receipt_pdf import render_to_pdf


# ================= HOME =================
def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
def add_donation(request):
    """Add new donation with images."""
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    form = DonationForm(request.POST or None)
    
    if request.method == "POST":

        
        # ✅ IMPORTANT FIX: handle missing amount
        if not amount or amount.strip() == "":
            amount = Decimal("0.00")
        else:
            amount = Decimal(amount)

        donation = Donation.objects.create(
            donor=request.user,
            category=category,
            description=description,
            pickup_date=pickup_date,
            amount=amount,        # ✅ FIXED
            status="Pending"
        )

        # Email confirmation
        if request.user.email:
            send_mail(
                subject="Donation Submitted Successfully – DonateHub",
                message=(
                    f"Hello {request.user.username},\n\n"
                    f"Thank you for your donation.\n\n"
                    f"Category: {donation.category}\n"
                    f"Amount: ₹{donation.amount}\n"
                    f"Pickup Date: {donation.pickup_date}\n\n"
                    f"Regards,\nDonateHub Team"
                ),
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=True,
=======
        if form.is_valid():
            donation = form.save(donor=request.user)
            
            # Create tracking record with initial timestamp
            from django.utils import timezone
            tracking = DonationTracking.objects.create(
                donation=donation,
                current_status=DonationStatus.SUBMITTED,
                submitted_at=timezone.now()

            )
            
            # Save multiple images
            images = request.FILES.getlist('images')
            for image in images:
                if image.content_type.startswith('image/'):
                    if image.size <= 5 * 1024 * 1024:  # 5MB limit
                        DonationImage.objects.create(donation=donation, image=image)
            
            # Email confirmation
            if request.user.email:
                try:
                    send_mail(
                        subject="Donation Submitted Successfully - DonateHub",
                        message=(
                            f"Hello {request.user.username},\n\n"
                            f"Thank you for your donation.\n\n"
                            f"Category: {donation.category}\n"
                            f"Amount: ₹{donation.amount or 0}\n"
                            f"Location: {donation.get_location_display()}\n"
                            f"Pickup Date: {donation.pickup_date}\n"
                            f"Receipt: {donation.receipt_number}\n\n"
                            f"Track your donation at: {request.build_absolute_uri('/donation/' + str(donation.id) + '/track/')}\n\n"
                            f"Regards,\nDonateHub Team"
                        ),
                        from_email=None,
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass
            
            messages.success(request, "Donation added successfully!")
            return redirect('/my-donations/')
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'form': form,
        'districts': KERALA_DISTRICTS,
    }
    return render(request, 'add_donation.html', context)


@login_required
def my_donations(request):
    """Display list of donations for the current user."""
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    donations = Donation.objects.filter(donor=request.user).prefetch_related('images')
    return render(request, 'my_donations.html', {'donations': donations})


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
        logger.info("Starting Gemini AI category detection...")
        
        from google.genai import Client
        from google.genai import errors as genai_errors
        from dotenv import load_dotenv
        from pathlib import Path
        
        # Reload .env file directly
        BASE_DIR = Path(settings.BASE_DIR)
        load_dotenv(BASE_DIR / '.env', override=True)
        
        api_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        if not api_key:
            logger.error("GEMINI_API_KEY is missing!")
            raise ValueError("API key not set")
        
        logger.info(f"API key: {api_key[:20]}...")
        
        # Initialize client with API key
        client = Client(api_key=api_key)
        
        prompt = (
            "Choose ONE category from this list ONLY: "
            "Clothes, Books, Toys, Electronics, Furniture, Footwear, "
            "Educational Materials, Household Items. "
            f"Description: {description}. "
            "Response: category name only."
        )
        
        logger.info("Calling Gemini 2.5 Flash...")
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        except genai_errors.ClientError as api_error:
            error_msg = str(api_error)
            logger.error(f"Gemini API ClientError: {error_msg}")
            # Check for quota errors
            if "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower() or "429" in error_msg:
                return JsonResponse({
                    "category": fallback,
                    "error": "quota_exceeded",
                    "message": "Daily API quota exceeded. Using fallback categorization."
                }, status=200)
            elif "API_KEY_INVALID" in error_msg or "400" in error_msg or "expired" in error_msg.lower():
                return JsonResponse({
                    "category": fallback,
                    "error": "api_key_invalid",
                    "message": "API key is invalid or expired. Please check the API key."
                }, status=200)
            else:
                return JsonResponse({
                    "category": fallback,
                    "error": "api_error",
                    "message": f"API error: {error_msg[:100]}"
                }, status=200)
        
        logger.info(f"Response: {response.text}")
        
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
                logger.info(f"Matched: {key} -> {value}")
                return JsonResponse({"category": value})
        
        logger.info("No keyword match, returning fallback")
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Gemini API error: {error_msg}", exc_info=True)
        # Check for quota errors in general exceptions
        if "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower() or "429" in error_msg:
            return JsonResponse({
                "category": fallback,
                "error": "quota_exceeded",
                "message": "Daily API quota exceeded. Using fallback categorization."
            }, status=200)
        elif "API_KEY_INVALID" in error_msg or "400" in error_msg or "expired" in error_msg.lower():
            return JsonResponse({
                "category": fallback,
                "error": "api_key_invalid",
                "message": "API key is invalid or expired. Please check the API key."
            }, status=200)
    
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
    """Display donation tracking timeline."""
    donation = get_object_or_404(
        Donation.objects.prefetch_related('images'),
        id=donation_id
    )
    
    if donation.donor != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this donation.")
    
    tracking, created = DonationTracking.objects.get_or_create(donation=donation)
    tracking_steps = tracking.get_tracking_steps()
    progress_percentage = donation.get_progress_percentage()
    
    context = {
        'donation': donation,
        'tracking': tracking,
        'tracking_steps': tracking_steps,
        'progress_percentage': progress_percentage,
        'districts': KERALA_DISTRICTS,
    }
    
    return render(request, 'donation_tracking.html', context)


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
    """Custom admin dashboard for managing donations."""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Admin access required.")
    
    # Get donation statistics
    total_donations = Donation.objects.count()
    pending_donations = Donation.objects.filter(status='pending').count()
    approved_donations = Donation.objects.filter(status='approved').count()
    completed_donations = Donation.objects.filter(status='completed').count()
    
    # Recent donations
    recent_donations = Donation.objects.prefetch_related('images', 'donor').order_by('-created_at')[:10]
    
    # Pending donations for quick action
    pending_list = Donation.objects.filter(status='pending').prefetch_related('images', 'donor').order_by('-created_at')[:5]
    
    context = {
        'total_donations': total_donations,
        'pending_donations': pending_donations,
        'approved_donations': approved_donations,
        'completed_donations': completed_donations,
        'recent_donations': recent_donations,
        'pending_list': pending_list,
    }
    
    return render(request, 'admin/dashboard.html', context)


# ================= API: GET DISTRICTS =================
def get_districts_json(request):
    """Return list of Kerala districts as JSON."""
    data = [{'id': name, 'name': name} for name, display in KERALA_DISTRICTS]
    return JsonResponse(data)


@login_required
def verify_otp(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    return render(request, "verify_otp.html", {"donation": donation})
