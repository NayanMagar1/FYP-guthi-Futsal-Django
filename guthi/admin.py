from django.contrib import admin
from .models import HomeSlider, futsal, Contact

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(futsal)
class futsalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_hour', 'peak_price', 'weekend_price')

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'location', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('price_per_hour', 'peak_price', 'weekend_price')
        }),
        ('Peak Hours', {
            'fields': ('peak_start', 'peak_end')
        }),
    )




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')

# admin.py
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


