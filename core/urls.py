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
    admin_dashboard,
)
from .api_views import (
    RegisterView, UserDetailView, DonationListCreateView, DonationDetailView
)
from .api_social import social_auth_callback
from .api_otp_auth import (
    SendOTPView, VerifyOTPView, ForgotPasswordView, ResetPasswordView, ReceiptPDFView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api_views import AdminStatsView

urlpatterns = [
    # ... previous paths ...
    path('api/donations/<int:donation_id>/send-otp/', SendOTPView.as_view(), name='api_send_otp'),
    path('api/donations/<int:donation_id>/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/receipt/<int:donation_id>/pdf/', ReceiptPDFView.as_view(), name='receipt-pdf'),
    path('api/auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('api/auth/reset-password/', ResetPasswordView.as_view(), name='api_reset_password'),
    path('api/admin/stats/', AdminStatsView.as_view(), name='api_admin_stats'),

    path('', home, name='home'),
    path('register/', register, name='register'),
    path('add/', add_donation, name='add_donation'),
    path('my-donations/', my_donations, name='my_donations'),

    # Admin Dashboard
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    # Donation tracking
    path('donation/<int:donation_id>/track/', donation_tracking, name='donation_tracking'),

    # Location API - Kerala districts (JSON)
    path('api/districts/', get_districts_json, name='get_districts_json'),

    # Admin status update
    path('admin/update-status/<int:donation_id>/', update_status, name='update_status'),

    # PDF receipt download
    path('receipt/<int:donation_id>/pdf/', download_receipt, name='receipt_pdf'),

    # AI endpoint (GET)
    path('api/ai-category/', ai_category, name='ai_category'),

    # API Endpoints
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', UserDetailView.as_view(), name='api_user_detail'),
    path('api/donations/', DonationListCreateView.as_view(), name='api_donations'),
    path('api/donations/<int:pk>/', DonationDetailView.as_view(), name='api_donation_detail'),
    path('api/social-callback/', social_auth_callback, name='social_auth_callback'),
]
