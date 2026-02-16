from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    

    class booking(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
        phone = models.CharField(max_length=20)
        date = models.DateField()
        time = models.TimeField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Booking by {self.name} on {self.date} at {self.time}"