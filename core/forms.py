from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Donation, DonationImage, KERALA_DISTRICTS


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DonationForm(forms.ModelForm):
    district = forms.ChoiceField(
        choices=[('', 'Select District')] + list(KERALA_DISTRICTS),
        required=False,
        label="District",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )

    area = forms.CharField(
        max_length=200,
        required=False,
        label="Area/Locality",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your locality, street name, or landmark'
        }),
        help_text="Optional"
    )

    class Meta:
        model = Donation
        fields = [
            'category',
            'description',
            'district',
            'area',
            'pickup_address',
            'pickup_date',
            'amount'
        ]
        widgets = {
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter or select category',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your donation items...',
                'required': True
            }),
            'pickup_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Full address for pickup...'
            }),
            'pickup_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Estimated value (₹)'
            }),
        }

    def clean_district(self):
        district = self.cleaned_data.get('district')
        valid_districts = [d[0] for d in KERALA_DISTRICTS]
        if district and district not in valid_districts:
            raise ValidationError("Please select a valid Kerala district.")
        return district

    def save(self, donor, commit=True):
        donation = super().save(commit=False)
        donation.donor = donor
        donation.state = 'Kerala'
        
        if commit:
            donation.save()
        
        return donation


class DonationImageForm(forms.ModelForm):
    class Meta:
        model = DonationImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image size cannot exceed 5MB.")
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                raise ValidationError("Invalid file type.")
        return image


class DistrictSearchForm(forms.Form):
    district = forms.ChoiceField(
        choices=[('', 'All Districts')] + list(KERALA_DISTRICTS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
