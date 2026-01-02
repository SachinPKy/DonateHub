from django.contrib import admin
from .models import Donation


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

