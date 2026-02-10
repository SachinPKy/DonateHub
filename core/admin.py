from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Donation, DonationImage, DonationTracking, DonationStatus


# ================= INLINE: Donation Images =================
class DonationImageInline(admin.TabularInline):
    model = DonationImage
    extra = 0
    readonly_fields = ('uploaded_at',)
    fields = ('image', 'uploaded_at')


# ================= ADMIN ACTION: Send OTP =================
def send_otp_action(modeladmin, request, queryset):
    """Admin action to send OTP to donors."""
    from .views import generate_otp
    from django.core.mail import send_mail
    from django.conf import settings
    from django.utils import timezone
    
    sent_count = 0
    for donation in queryset:
        # Generate OTP
        otp = generate_otp()
        donation.otp = otp
        donation.otp_created_at = timezone.now()
        donation.otp_verified = False
        donation.save()
        
        # Send OTP via email
        user_email = donation.donor.email
        if user_email:
            try:
                send_mail(
                    subject="Your OTP for Donation Verification - DonateHub",
                    message=(
                        f"Hello {donation.donor.username},\n\n"
                        f"Your OTP for donation verification is: {otp}\n\n"
                        f"This OTP is valid for 10 minutes.\n\n"
                        f"Donation Details:\n"
                        f"Category: {donation.category}\n"
                        f"Receipt: {donation.receipt_number}\n\n"
                        f"Please share this OTP with the admin when requested.\n\n"
                        f"Regards,\nDonateHub Team"
                    ),
                    from_email=getattr(settings, 'EMAIL_HOST_USER', None),
                    recipient_list=[user_email],
                    fail_silently=True,
                )
                sent_count += 1
                messages.success(request, f"OTP sent to {user_email} for donation #{donation.id}")
            except Exception as e:
                messages.error(request, f"Failed to send OTP for donation #{donation.id}: {e}")
        else:
            messages.warning(request, f"No email found for donation #{donation.id}")
    
    if sent_count == 0:
        messages.warning(request, "No OTPs were sent (no valid email addresses).")

send_otp_action.short_description = "Send OTP to selected donors"


# ================= ADMIN ACTION: Verify OTP =================
def verify_otp_action(modeladmin, request, queryset):
    """Admin action to verify OTP for selected donations."""
    if queryset.count() != 1:
        messages.error(request, "Please select exactly one donation to verify OTP.")
        return
    
    donation = queryset.first()
    
    # Redirect to the OTP verification page
    return redirect('/admin/core/donation/verify_otp/%d/' % donation.id)

verify_otp_action.short_description = "Verify OTP (requires OTP input)"


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'donor',
        'category',
        'status',
        'pickup_date',
        'created_at',
    )

    list_filter = (
        'status',
        'category',
        'pickup_date',
    )

    search_fields = (
        'donor__username',
        'category',
        'description',
    )

    list_editable = ('status',)

    ordering = ('-created_at',)

    inlines = [DonationImageInline]

    actions = [send_otp_action, verify_otp_action]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'verify_otp/<int:donation_id>/',
                self.admin_site.admin_view(self.verify_otp),
                name='verify_otp',
            ),
        ]
        return custom_urls + urls

    def verify_otp(self, request, donation_id):
        """Custom admin view to verify OTP for a donation."""
        donation = get_object_or_404(Donation, id=donation_id)
        
        if request.method == 'POST':
            entered_otp = request.POST.get('otp', '').strip()
            
            # Check if OTP matches
            if donation.otp and entered_otp == donation.otp:
                # Check if OTP is still valid (10 minutes)
                from django.utils import timezone
                if donation.otp_created_at:
                    time_diff = timezone.now() - donation.otp_created_at
                    if time_diff.total_seconds() > 600:  # 10 minutes = 600 seconds
                        messages.error(request, "OTP has expired. Please request a new OTP.")
                        return redirect('/admin/core/donation/')
                
                donation.otp_verified = True
                donation.save()
                messages.success(request, f"OTP verified successfully for donation #{donation.id}")
                return redirect('/admin/core/donation/')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        
        return render(request, 'admin/verify_otp.html', {
            'donation': donation,
        })

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Donation.objects.get(pk=obj.pk)

            # Auto-generate OTP ONLY when approving
            if old_obj.status != 'Approved' and obj.status == 'Approved':
                import random
                from django.utils import timezone
                obj.otp = str(random.randint(100000, 999999))
                obj.otp_created_at = timezone.now()
                obj.otp_verified = False

        super().save_model(request, obj, form, change)
