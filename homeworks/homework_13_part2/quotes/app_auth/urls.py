from django.urls import path
from . import views

app_name = "app_auth"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("login/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("password_reset/", views.AppPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.AppPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.AppPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.AppPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
