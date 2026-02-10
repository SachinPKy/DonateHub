from django.contrib import admin
from django.contrib.auth.models import User

from .models import Donation, DonationImage, DonationTracking, DonationStatus


# ================= INLINE: Donation Images =================
class DonationImageInline(admin.TabularInline):
    model = DonationImage
    extra = 0
    readonly_fields = ('uploaded_at',)
    fields = ('image', 'uploaded_at')


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
    )
    
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
