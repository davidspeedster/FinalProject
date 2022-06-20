from django.urls import path
from .views import PersonnelSignupView, HospitalSignupView, AdminSignupView, UserLoginView, LogoutAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView
app_name = 'authentication'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logouts'),
    path('register_personnel/', PersonnelSignupView.as_view(),
         name='register_personnel'),
    path('register_hospital/', HospitalSignupView.as_view(),
         name='register_hospital'),
    path('register_admin/', AdminSignupView.as_view(),
         name='register_admin'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')

]
