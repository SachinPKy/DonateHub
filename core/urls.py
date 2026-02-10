from django.urls import path
from .views import (
    home,
    register,
    add_donation,
    my_donations,
    ai_category,
    update_status,
    download_receipt,
    donation_tracking,
    get_districts_json,
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('add/', add_donation, name='add_donation'),
    path('my-donations/', my_donations, name='my_donations'),

    # Donation tracking
    path('donation/<int:donation_id>/track/', donation_tracking, name='donation_tracking'),

    # Location API - Kerala districts (JSON)
    path('api/districts/', get_districts_json, name='get_districts_json'),

    # Admin status update
    path('admin/update-status/<int:donation_id>/', update_status, name='update_status'),

    # PDF receipt download
    path('receipt/<int:donation_id>/pdf/', download_receipt, name='receipt_pdf'),

    # AI endpoint (GET)
    path('ai-category/', ai_category, name='ai_category'),
]
