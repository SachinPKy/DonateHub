from django.urls import path
from .views import (
    home,
    register,
    add_donation,
    my_donations,
    ai_category
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('add/', add_donation, name='add_donation'),
    path('my-donations/', my_donations, name='my_donations'),

    # AI endpoint (GET)
    path('ai-category/', ai_category, name='ai_category'),
]
