from django.db import models


class HomeSlider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='home_slider/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title