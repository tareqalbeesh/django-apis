"""
URL configuration for FinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.authtoken'),),
    # login using djoser's token authentication would be possible under api/token/login/
    # DRF's built in token authentication method
    path('token/login/', obtain_auth_token),
    # djangorestframework-simpleJWT JWT authentication (session/refresh keys)
    path('jwt-auth/', TokenObtainPairView.as_view()),
    path('jwt-auth/refresh', TokenRefreshView.as_view()),
    path('jwt-auth/blacklist/', TokenBlacklistView.as_view()),
    path('api/', include('API.urls'))
]
