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
    """Admin action to send OTP to donors for pickup/delivery verification."""
    import random
    from django.core.mail import send_mail
    from django.conf import settings
    from django.utils import timezone
    
    sent_count = 0
    for donation in queryset:
        # Generate OTP
        otp = str(random.randint(100000, 999999))
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


# ================= ADMIN: Donation =================
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'donor',
        'category',
        'district',
        'status',
        'pickup_date',
        'receipt_number',
        'otp_verified',
        'created_at',
    )
    
    list_filter = (
        'status',
        'district',
        'pickup_date',
        'created_at',
    )
    
    search_fields = (
        'donor__username',
        'donor__email',
        'category',
        'description',
        'area',
        'receipt_number',
    )
    
    list_editable = ('status', 'district')
    
    ordering = ('-created_at',)
    
    inlines = [
        DonationImageInline,
    ]
    
    readonly_fields = (
        'state',
        'created_at',
        'updated_at',
        'receipt_number',
        'otp',
        'otp_verified',
    )
    
    actions = [send_otp_action, verify_otp_action]

    def save_model(self, request, obj, form, change):
        """Override save to update tracking when status changes."""
        if change:
            old_obj = Donation.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                # Status changed - update tracking
                from django.utils import timezone
                from .models import DonationTracking
                tracking, created = DonationTracking.objects.get_or_create(donation=obj)
                tracking.current_status = obj.status
                # Set the appropriate timestamp based on new status
                status_timestamp_map = {
                    DonationStatus.SUBMITTED: 'submitted_at',
                    DonationStatus.CONFIRMED: 'confirmed_at',
                    DonationStatus.PICKUP_SCHEDULED: 'pickup_scheduled_at',
                    DonationStatus.PICKED_UP: 'picked_up_at',
                    DonationStatus.IN_TRANSIT: 'in_transit_at',
                    DonationStatus.DELIVERED: 'delivered_at',
                    DonationStatus.COMPLETED: 'completed_at',
                }
                timestamp_field = status_timestamp_map.get(obj.status)
                if timestamp_field and not getattr(tracking, timestamp_field):
                    setattr(tracking, timestamp_field, timezone.now())
                tracking.save()
        super().save_model(request, obj, form, change)

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
                # Update donation status to PICKED_UP after OTP verification
                donation.status = DonationStatus.PICKED_UP
                donation.save()
                
                # Update tracking record
                from .models import DonationTracking
                tracking, created = DonationTracking.objects.get_or_create(donation=donation)
                tracking.save()
                
                messages.success(request, f"OTP verified successfully for donation #{donation.id}. Status updated to Picked Up.")
                return redirect('/admin/core/donation/')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        
        return render(request, 'admin/verify_otp.html', {
            'donation': donation,
        })

    fieldsets = (
        ('Donor & Category', {
            'fields': ('donor', 'category', 'description', 'amount', 'receipt_number')
        }),
        ('Location (Kerala Only)', {
            'fields': ('state', 'district', 'area', 'pickup_address'),
            'description': 'State is fixed to Kerala. Select district from dropdown.'
        }),
        ('Status & Tracking', {
            'fields': ('status', 'pickup_date', 'created_at', 'updated_at')
        }),
        ('OTP Verification', {
            'fields': ('otp', 'otp_created_at', 'otp_verified'),
            'classes': ('collapse',),
        }),
    )


# ================= ADMIN: Donation Image =================
@admin.register(DonationImage)
class DonationImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'donation',
        'donation_donor',
        'uploaded_at',
    )
    
    list_filter = ('uploaded_at',)
    
    search_fields = (
        'donation__id',
        'donation__donor__username',
    )
    
    readonly_fields = ('uploaded_at',)
    
    def donation_donor(self, obj):
        return obj.donation.donor.username
    
    donation_donor.short_name = 'Donor'


# ================= ADMIN: Donation Tracking =================
@admin.register(DonationTracking)
class DonationTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'donation',
        'donation_donor',
        'current_status',
        'updated_at',
    )
    
    list_filter = (
        'current_status',
        'updated_at',
    )
    
    search_fields = (
        'donation__id',
        'donation__donor__username',
    )
    
    readonly_fields = (
        'donation',
        'current_status',
        'updated_at',
        'submitted_at',
        'confirmed_at',
        'pickup_scheduled_at',
        'picked_up_at',
        'in_transit_at',
        'delivered_at',
        'completed_at',
    )
    
    def donation_donor(self, obj):
        return obj.donation.donor.username
    
    donation_donor.short_name = 'Donor'
