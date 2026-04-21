from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.mail import send_mail
from django.conf import settings

from guthi.models import Booking


class Command(BaseCommand):
    help = 'Send booking reminders 1 hour before game'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # Time range (1 hour from now)
        reminder_time_start = now + timedelta(minutes=55)
        reminder_time_end = now + timedelta(minutes=65)

        bookings = Booking.objects.filter(
            is_paid=True,
            email_sent=False
        )

        for booking in bookings:
            booking_datetime = datetime.combine(booking.date, booking.time)
            booking_datetime = timezone.make_aware(booking_datetime)

            if reminder_time_start <= booking_datetime <= reminder_time_end:

                if booking.user and booking.user.email:
                    send_mail(
                        subject='⏰ Reminder: Your Futsal Game in 1 Hour',
                        message=f"""
Hello {booking.user.username},

Reminder! Your futsal game is in 1 hour.

Futsal: {booking.futsal.name}
Date: {booking.date}
Time: {booking.time}

Don't be late! ⚽
""",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[booking.user.email],
                        fail_silently=False,
                    )

                    # Mark as sent
                    booking.email_sent = True
                    booking.save()

                    self.stdout.write(f"Reminder sent to {booking.user.email}")