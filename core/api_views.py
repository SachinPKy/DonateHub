from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Donation, DonationImage, DonationTracking
from .serializers import (
    UserSerializer, RegisterSerializer, DonationSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

from django.core.mail import send_mail

class DonationListCreateView(generics.ListCreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user)

    def perform_create(self, serializer):
        donation = serializer.save(donor=self.request.user)
        # Handle images if provided in request.FILES
        images = self.request.FILES.getlist('images')
        for image in images:
            DonationImage.objects.create(donation=donation, image=image)
        # Create tracking entry
        DonationTracking.objects.create(donation=donation)

        # Restore Email confirmation service
        if self.request.user.email:
            try:
                send_mail(
                    subject="Donation Received - DonateHub",
                    message=(
                        f"Hello {self.request.user.username},\n\n"
                        f"We have received your donation request.\n\n"
                        f"Category: {donation.category}\n"
                        f"Location: {donation.area}\n"
                        f"Pickup Date: {donation.pickup_date}\n\n"
                        f"Track it here: http://localhost:5173/tracking/{donation.id}\n\n"
                        f"Regards,\nDonateHub Team"
                    ),
                    from_email=None,
                    recipient_list=[self.request.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass

class DonationDetailView(generics.RetrieveAPIView):
    serializer_class = DonationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user)

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
class AdminStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"error": "Admin access required."}, status=status.HTTP_403_FORBIDDEN)
        
        stats = {
            "total": Donation.objects.count(),
            "pending": Donation.objects.filter(status='SUBMITTED').count(),
            "approved": Donation.objects.filter(status='CONFIRMED').count(),
            "completed": Donation.objects.filter(status='COMPLETED').count(),
            "recent": DonationSerializer(Donation.objects.all().order_by('-created_at')[:10], many=True).data
        }
        return Response(stats)
