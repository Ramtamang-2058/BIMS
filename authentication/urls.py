from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    AuthUserRegistrationView,
    AuthUserLoginView,
    UserListView,
    LogoutAPIView,
RequestPasswordResetEmail,
SetNewPasswordAPIView,
PasswordTokenCheckAPI,
ChangePasswordView

)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', AuthUserRegistrationView.as_view(), name='register'),
    path('login', AuthUserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('change_password/', ChangePasswordView.as_view(), name="change-password"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),

]