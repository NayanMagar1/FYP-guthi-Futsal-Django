from django.db import models


class HomeSlider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='home_slider/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class futsal(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='futsal_images/')   
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    futsal = models.ForeignKey(futsal, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.futsal.name} - {self.date} - {self.time}"
    
