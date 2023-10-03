from django.db import models

# Create your models here.

class ScheduledMessage(models.Model):
    body = models.TextField()
    recipient = models.CharField(max_length=255)  # Store recipient's WhatsApp number
    scheduled_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
