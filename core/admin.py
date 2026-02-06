from django.contrib import admin
from .models import Donation
import random


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

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Donation.objects.get(pk=obj.pk)

            # Auto-generate OTP ONLY when approving
            if old_obj.status != 'Approved' and obj.status == 'Approved':
                obj.otp = str(random.randint(100000, 999999))
                obj.otp_verified = False

        super().save_model(request, obj, form, change)
