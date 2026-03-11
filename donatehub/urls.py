from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import social_login_cancelled, social_login_error, home

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Intercept allauth views that lead to old templates
    path('accounts/login/', home, name='account_login'),
    path('accounts/social/login/cancelled/', social_login_cancelled, name='socialaccount_login_cancelled'),
    path('accounts/social/login/error/', social_login_error, name='socialaccount_login_error'),
    
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
