from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path("register/", views.register_view, name="register"),
    
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("aboutus/", views.about_us, name="aboutus"),
    path("contactus/", views.contact_us, name="contactus"),
    path('futsals/', views.futsal_list, name='futsal_list'),
    path('futsal/<int:id>/', views.futsal_detail, name='futsal_detail'),
    path('khalti/payment/', views.khalti_payment, name='khalti_payment'),
    path('khalti/verify/', views.khalti_verify, name='khalti_verify'),
    path('profile/', views.profile_view, name='profile'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('profile/change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/profile/'), name='change_password'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
