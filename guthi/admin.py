from django.contrib import admin
from .models import HomeSlider, futsal, Contact

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(futsal)
class futsalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at','image')




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')

# admin.py
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


