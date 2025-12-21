from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

import google.generativeai as genai

from .models import Donation
from .forms import RegisterForm


# ================= GEMINI CONFIG =================
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


# ================= HOME =================
def home(request):
    # Admin users should directly use admin panel
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
    # Prevent admin from donating as normal user
    if request.user.is_superuser:
        return redirect('/admin/')

    if request.method == "POST":
        donation = Donation.objects.create(
            donor=request.user,
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            pickup_date=request.POST.get('pickup_date')
        )

        # Email confirmation (optional but professional)
        if request.user.email:
            send_mail(
                subject="Donation Submitted Successfully – DonateHub",
                message=(
                    f"Hello {request.user.username},\n\n"
                    f"Thank you for your donation.\n\n"
                    f"Category: {donation.category}\n"
                    f"Pickup Date: {donation.pickup_date}\n\n"
                    f"Regards,\nDonateHub Team"
                ),
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

        return render(request, 'success.html')

    return render(request, 'add_donation.html')


# ================= MY DONATIONS =================
@login_required
def my_donations(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    donations = Donation.objects.filter(donor=request.user)
    return render(request, 'my_donations.html', {'donations': donations})


# ================= GEMINI AI CATEGORY (GET BASED) =================
def ai_category(request):
    description = request.GET.get('description', '').lower()

    # -------- RULE-BASED FALLBACK (ALWAYS SAFE) --------
    fallback = "Household Items"
    if "book" in description or "textbook" in description or "notebook" in description:
        fallback = "Books"
    elif "toy" in description:
        fallback = "Toys"
    elif "laptop" in description or "mobile" in description or "charger" in description:
        fallback = "Electronics"
    elif "shoe" in description or "slipper" in description:
        fallback = "Footwear"
    elif "shirt" in description or "pant" in description or "jacket" in description:
        fallback = "Clothes"
    elif "table" in description or "chair" in description:
        fallback = "Furniture"

    # -------- GEMINI AI --------
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

        for key in categories:
            if key in ai_text:
                return JsonResponse({"category": categories[key]})

    except Exception as e:
        # Gemini failure should NEVER break the system
        print("Gemini failed, using fallback:", e)

    return JsonResponse({"category": fallback})
