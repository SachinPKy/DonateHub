from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import logging

from decimal import Decimal
import random
import google.generativeai as genai

from .models import Donation
from .forms import RegisterForm
from .utils.receipt_pdf import render_to_pdf

logger = logging.getLogger(__name__)


# ================= OTP GENERATOR =================
def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))


# ================= GEMINI CONFIG =================
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


# ================= HOME =================
def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin/')
    return render(request, 'home.html')


# ================= REGISTER =================
def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/accounts/login/')

    return render(request, 'register.html', {'form': form})


# ================= ADD DONATION =================
@login_required
def add_donation(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    if request.method == "POST":
        category = request.POST.get('category')
        description = request.POST.get('description')
        pickup_date = request.POST.get('pickup_date')
        amount = request.POST.get('amount')
        photo = request.FILES.get("photo")

        # Handle missing or empty amount
        if not amount or amount.strip() == "":
            amount = Decimal("0.00")
        else:
            amount = Decimal(amount)

        donation = Donation.objects.create(
            donor=request.user,
            category=category,
            description=description,
            pickup_date=pickup_date,
            amount=amount,
            status="Pending",
            photo=photo
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
            )

        messages.success(request, "Donation added successfully.")
        return redirect('/my-donations/')

    return render(request, 'add_donation.html')


# ================= MY DONATIONS =================
@login_required
def my_donations(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    donations = Donation.objects.filter(donor=request.user)
    return render(request, 'my_donations.html', {'donations': donations})


# ================= OTP VERIFICATION =================
@login_required
def verify_otp(request, donation_id):
    if request.user.is_superuser:
        return redirect('/admin/')

    donation = get_object_or_404(Donation, id=donation_id)

    if donation.status != "Approved":
        messages.error(request, "Donation is not approved yet.")
        return redirect('/my-donations/')

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if entered_otp == donation.otp:
            donation.otp_verified = True
            donation.status = "Picked Up"
            donation.save()

            messages.success(request, "OTP verified. Donation picked up successfully.")
            return render(request, "success.html")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "verify_otp.html", {"donation": donation})


# ================= GEMINI AI CATEGORY =================
def ai_category(request):
    description = request.GET.get('description', '').lower()

    fallback = "Household Items"
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
        print("Gemini failed, using fallback:", e)

    return JsonResponse({"category": fallback})


# ================= DOWNLOAD RECEIPT (PDF) =================
@login_required
def download_receipt(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.donor != request.user:
        return HttpResponseForbidden("You are not authorized to download this receipt.")

    context = {
        "donation": donation,
        "donation_id": donation.id,
        "generated_date": timezone.now(),
    }

    response = render_to_pdf("receipt.html", context)

    donation.receipt_generated_at = timezone.now()
    donation.save(update_fields=["receipt_generated_at"])

    return response
