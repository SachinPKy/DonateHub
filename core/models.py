from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


# Kerala Districts Constant
KERALA_DISTRICTS = [
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Kollam', 'Kollam'),
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Alappuzha', 'Alappuzha'),
    ('Kottayam', 'Kottayam'),
    ('Idukki', 'Idukki'),
    ('Ernakulam', 'Ernakulam'),
    ('Thrissur', 'Thrissur'),
    ('Palakkad', 'Palakkad'),
    ('Malappuram', 'Malappuram'),
    ('Kozhikode', 'Kozhikode'),
    ('Wayanad', 'Wayanad'),
    ('Kannur', 'Kannur'),
    ('Kasaragod', 'Kasaragod'),
]


class DonationStatus:
    SUBMITTED = 'SUBMITTED'
    CONFIRMED = 'CONFIRMED'
    PICKUP_SCHEDULED = 'PICKUP_SCHEDULED'
    PICKED_UP = 'PICKED_UP'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'

    CHOICES = [
        (SUBMITTED, 'Submitted'),
        (CONFIRMED, 'Confirmed'),
        (PICKUP_SCHEDULED, 'Pickup Scheduled'),
        (PICKED_UP, 'Picked Up'),
        (IN_TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    # For progress bar ordering
    ORDER = [
        SUBMITTED,
        CONFIRMED,
        PICKUP_SCHEDULED,
        PICKED_UP,
        IN_TRANSIT,
        DELIVERED,
        COMPLETED,
    ]

    # Terminal statuses
    TERMINAL = [COMPLETED, DELIVERED, CANCELLED]


def generate_receipt_number():
    """Generate unique receipt number."""
    return f"RCPT-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    category = models.CharField(max_length=100)
    description = models.TextField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    pickup_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Status with new choices
    status = models.CharField(
        max_length=20,
        choices=DonationStatus.CHOICES,
        default=DonationStatus.SUBMITTED
    )
    
    # Receipt - unique and auto-generated
    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )
    
    # Kerala Location (no FK tables)
    state = models.CharField(max_length=50, default='Kerala', editable=False)
    district = models.CharField(
        max_length=50,
        choices=KERALA_DISTRICTS,
        blank=True,
        null=True
    )
    area = models.CharField(max_length=200, blank=True, null=True)
    pickup_address = models.TextField(blank=True, null=True)
    
    # OTP Verification for Pickup/Delivery
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def generate_otp(self):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.category} - {self.status}"

    def save(self, *args, **kwargs):
        # Generate receipt number if not exists
        if not self.receipt_number:
            self.receipt_number = generate_receipt_number()
        super().save(*args, **kwargs)

    def get_location_display(self):
        """Get formatted location string."""
        parts = []
        if self.area:
            parts.append(self.area)
        if self.district:
            parts.append(self.district)
        parts.append(self.state)
        return ' → '.join(parts) if parts else self.state

    def get_progress_percentage(self):
        """Calculate progress percentage for progress bar."""
        if self.status == DonationStatus.CANCELLED:
            return 0
        if self.status in DonationStatus.TERMINAL:
            return 100
        try:
            current_idx = DonationStatus.ORDER.index(self.status)
            return int((current_idx / len(DonationStatus.ORDER)) * 100)
        except (ValueError, IndexError):
            return 0

    def get_current_step(self):
        """Get current tracking step index."""
        if self.status in DonationStatus.ORDER:
            return DonationStatus.ORDER.index(self.status)
        return 0


class DonationImage(models.Model):
    donation = models.ForeignKey(
        Donation, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='donations/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for {self.donation.id}"


class DonationTracking(models.Model):
    """Professional tracking with OneToOneField to donation."""
    donation = models.OneToOneField(
        Donation, 
        on_delete=models.CASCADE, 
        related_name='tracking'
    )
    current_status = models.CharField(
        max_length=20,
        choices=DonationStatus.CHOICES,
        default=DonationStatus.SUBMITTED
    )
    updated_at = models.DateTimeField(auto_now=True)

    # Status history
    submitted_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    pickup_scheduled_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    in_transit_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Donation tracking'

    def __str__(self):
        return f"Tracking: {self.donation.id} - {self.current_status}"

    def save(self, *args, **kwargs):
        # Sync current_status with donation status
        if self.donation:
            self.current_status = self.donation.status
        # Update timestamp based on status
        self._update_timestamp()
        super().save(*args, **kwargs)

    def _update_timestamp(self):
        """Update timestamp based on current status."""
        now = timezone.now()
        status_map = {
            DonationStatus.SUBMITTED: 'submitted_at',
            DonationStatus.CONFIRMED: 'confirmed_at',
            DonationStatus.PICKUP_SCHEDULED: 'pickup_scheduled_at',
            DonationStatus.PICKED_UP: 'picked_up_at',
            DonationStatus.IN_TRANSIT: 'in_transit_at',
            DonationStatus.DELIVERED: 'delivered_at',
            DonationStatus.COMPLETED: 'completed_at',
        }
        field_name = status_map.get(self.current_status)
        if field_name and not getattr(self, field_name):
            setattr(self, field_name, now)

    def get_tracking_steps(self):
        """Get ordered tracking steps with timestamps."""
        steps = []
        for idx, status in enumerate(DonationStatus.ORDER):
            status_label = dict(DonationStatus.CHOICES).get(status, status)
            timestamp = getattr(self, f"{status.lower()}_at", None)
            completed = getattr(self, f"{status.lower()}_at", None) is not None
            # Use donation's status for is_current to ensure accuracy
            donation_status = self.donation.status if self.donation else self.current_status
            is_current = status == donation_status
            
            steps.append({
                'status': status,
                'label': status_label,
                'timestamp': timestamp,
                'completed': completed,
                'is_current': is_current,
                'step_number': idx + 1,
            })
        return steps



