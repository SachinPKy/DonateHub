from django.urls import path
from .views import (
    home,
    register,
    add_donation,
    my_donations,
    ai_category,
    verify_otp,
    download_receipt,
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('add/', add_donation, name='add_donation'),
    path('my-donations/', my_donations, name='my_donations'),

    # OTP verification
    path('verify-otp/<int:donation_id>/', verify_otp, name='verify_otp'),

    # PDF receipt download
    path('receipt/<int:donation_id>/pdf/', download_receipt, name='receipt_pdf'),

    # AI endpoint (GET)
    path('ai-category/', ai_category, name='ai_category'),
]
