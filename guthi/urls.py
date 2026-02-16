from django.urls import path
from . import views

urlpatterns = [
    
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("aboutus/", views.about_us, name="aboutus"),
    path("contactus/", views.contact_us, name="contactus"),
]
