from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("aboutus/", views.about_us, name="aboutus"),
    path("contactus/", views.contact_us, name="contactus"),
    path('futsals/', views.futsal_list, name='futsal_list'),
    path('futsal/<int:id>/', views.futsal_detail, name='futsal_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
