from django.contrib import admin
from .models import HomeSlider, futsal

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(futsal)
class futsalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at','image')


