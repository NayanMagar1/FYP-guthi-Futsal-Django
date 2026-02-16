from django.contrib import admin
from .models import HomeSlider

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
