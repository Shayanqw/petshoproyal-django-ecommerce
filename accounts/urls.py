from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('otpregister/', views.registerotp, name='otpregister'),
    # path('login/',views.user_login,name='login'),
    # path('otp/',views.otp_view,name='otp'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('update/', views.user_update, name='update'),
    path('change/', views.change_password, name='change'),
    path('verify/', views.verify, name='verify'),
    path('active/<uidb64>/<token>/', views.RegisterEmail.as_view(), name='active'),
    # path('reset/', views.ResetPassword.as_view(), name='reset'),
    path('reset/', views.resetpass, name='reset'),
    path('reset/done/', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>', views.ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(), name='compelet'),
    # path('favourite/',views.favourite,name='favourite'),
    # path('history/',views.history,name='history'),
    path('view/', views.product_view, name='product_view'),
    path('login/', views.LoginOTP.as_view(), name='login'),
    path('otp/', views.otp_view, name='otp'),
    path('resetotp/', views.resetpasswordotp, name='resetotp'),
    path('resetpassword/<uidb64>/<token>', views.resetpassword, name='resetpass'),
]
