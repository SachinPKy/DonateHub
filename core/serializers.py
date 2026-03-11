from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Donation, DonationImage, DonationTracking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_superuser')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class DonationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationImage
        fields = ('id', 'image', 'uploaded_at')

class DonationSerializer(serializers.ModelSerializer):
    images = DonationImageSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    location_display = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = (
            'id', 'category', 'description', 'pickup_date', 'amount', 
            'status', 'status_display', 'receipt_number', 
            'district', 'area', 'pickup_address', 'otp_verified',
            'created_at', 'images', 'location_display', 'progress_percentage', 'main_image'
        )
        read_only_fields = ('receipt_number', 'otp_verified', 'created_at')

    def get_main_image(self, obj):
        image = obj.images.first()
        if image and image.image:
            return image.image.url
        return None

    def get_location_display(self, obj):
        return f"{obj.area}, {obj.district}, Kerala"

    def get_progress_percentage(self, obj):
        from .models import DonationStatus
        order = DonationStatus.ORDER
        try:
            return int((order.index(obj.status) / (len(order) - 1)) * 100)
        except (ValueError, IndexError):
            return 0
