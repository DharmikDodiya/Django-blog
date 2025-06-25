# myapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document
from .tasks import send_notification_email

@receiver(post_save, sender=Document)
def document_uploaded(sender, instance, created, **kwargs):
    if created:
        print("Document uploaded:", instance)
        send_notification_email.delay(instance.id)