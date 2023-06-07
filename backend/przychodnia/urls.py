from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('patient.urls')),
    path('api/doctor/', include('doctor.urls')),
    path('api/reception/', include('reception.urls')),
]
