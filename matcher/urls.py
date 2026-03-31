from django.urls import path
from .views import GetMeView, LoginView, SetPasswordView, UserProfileCreateView, UserProfileDetailView, MatchResultView, SendOTPView, VerifyOTPView

urlpatterns = [
    path('profile/', UserProfileCreateView.as_view(), name='create-profile'),
    path('profile/<str:email>/', UserProfileDetailView.as_view(), name='get-update-profile'),
    path('match-result/', MatchResultView.as_view(), name='match-result'), 
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
    path('auth/me/', GetMeView.as_view(), name='get-me'),
    path('auth/login/', LoginView.as_view(), name='login'),

]
