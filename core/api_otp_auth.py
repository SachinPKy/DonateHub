import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import Donation, DonationStatus, DonationTracking
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class SendOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, donation_id):
        # Only delivery agents (staff) or superusers can send OTP
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"error": "Only delivery agents can send OTP."}, status=status.HTTP_403_FORBIDDEN)

        donation = get_object_or_404(Donation, id=donation_id)
        
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        donation.otp = otp
        donation.otp_created_at = timezone.now()
        donation.otp_verified = False
        donation.save()

        # Send OTP via email to donor
        if donation.donor.email:
            try:
                context = {
                    'username': donation.donor.username,
                    'otp': otp,
                    'category': donation.category,
                    'receipt_number': donation.receipt_number,
                }
                html_message = render_to_string('email/email_otp.html', context)
                plain_message = strip_tags(html_message)

                send_mail(
                    subject="Your OTP for Donation Verification - DonateHub",
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[donation.donor.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                return Response({"message": f"OTP sent to {donation.donor.email}"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"error": "Donor has no email address."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, donation_id):
        donation = get_object_or_404(Donation, id=donation_id)
        entered_otp = request.data.get('otp', '').strip()

        if not donation.otp or entered_otp != donation.otp:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Check expiry (10 minutes)
        if donation.otp_created_at:
            time_diff = timezone.now() - donation.otp_created_at
            if time_diff.total_seconds() > 600:
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        donation.otp_verified = True
        # If OTP is for delivery, update status
        donation.status = DonationStatus.DELIVERED
        donation.save()

        # Update tracking
        tracking, created = DonationTracking.objects.get_or_create(donation=donation)
        tracking.save()

        return Response({"message": "OTP verified successfully. Donation marked as Delivered."}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
            
            try:
                context = {
                    'username': user.username,
                    'reset_link': reset_link,
                }
                html_message = render_to_string('email/email_password_reset.html', context)
                plain_message = strip_tags(html_message)

                send_mail(
                    subject="Password Reset Request - DonateHub",
                    message=plain_message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # For security, always return success even if user doesn't exist
        return Response({"message": "If an account exists with this email, a reset link has been sent."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('password')

        if not all([uidb64, token, new_password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful. You can now login."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

class ReceiptPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, donation_id):
        try:
            donation = Donation.objects.get(id=donation_id)
            # Only donor or staff can download receipt
            if donation.donor != request.user and not request.user.is_staff:
                return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
            context = {
                'donation': donation,
                'donation_id': donation.id,
                'receipt_number': donation.receipt_number,
                'donor_name': donation.donor.username,
                'category': donation.category,
                'description': donation.description,
                'area': donation.area,
                'district': donation.district,
                'status': donation.get_status_display(),
                'pickup_date': donation.pickup_date,
                'created_at': donation.created_at,
            }
            
            from core.utils.receipt_pdf import render_to_pdf
            return render_to_pdf('admin/receipt_pdf.html', context)
            
        except Donation.DoesNotExist:
            return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
