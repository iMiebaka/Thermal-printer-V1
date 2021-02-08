from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("view-profile/", views.view_profile, name="view_profile"),
    path("logout/", views.logout_view, name="logout_view"),    
    path("ajax/validate-username/", views.validate_username, name="validate_username"),
]