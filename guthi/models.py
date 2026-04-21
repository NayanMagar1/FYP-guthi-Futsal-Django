from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


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

    price_per_hour = models.IntegerField(default=1000)

    # 🔥 Dynamic pricing
    peak_start = models.TimeField(null=True, blank=True)
    peak_end = models.TimeField(null=True, blank=True)

    peak_price = models.IntegerField(default=1500)
    weekend_price = models.IntegerField(default=1200)

    def __str__(self):
        return self.name


class Booking(models.Model):
    futsal = models.ForeignKey(futsal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    date = models.DateField()
    time = models.TimeField()

    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    email_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('futsal', 'date', 'time')

    def __str__(self):
        return f"{self.futsal.name} - {self.date} - {self.time}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    



# Profile model for user info
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.png')
    full_name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


# Automatically create/update Profile when User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
