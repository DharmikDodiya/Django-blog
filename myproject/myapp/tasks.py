# myapp/tasks.py
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging
from .models import Document  # import inside task to avoid circular import
import os
from django.conf import settings

logger = logging.getLogger(__name__)

# @shared_task
# def send_notification_email(document_id):
#     try:
#         document = Document.objects.select_related('user').get(pk=document_id)
#         subject = 'New Document Uploaded'
#         from_email = 'hello@google.com'
#         to_email = [document.user.email]
#         html_content = render_to_string('emails/file_upload.html', {'title': document.title})
#         email = EmailMultiAlternatives(subject, '', from_email, to_email)
#         email.attach_alternative(html_content, "text/html")
#         email.send()
#         print("Email sent!")
#     except Exception as e:
#         logger.error(f"Error sending email: {e}")
#         print(f"Email error: {e}")


@shared_task
def send_notification_email(document_id):
    try:
        # Get the uploaded document and user
        document = Document.objects.select_related('user').get(pk=document_id)

        subject = 'New Document Uploaded'
        from_email = 'hello@google.com'  # replace with your actual sender address
        to_email = [document.user.email]

        # Construct public download URL if needed
        # document_url = f"{settings.DOMAIN}{document.file.url}" if document.file else None

        # Render the email content
        html_content = render_to_string('emails/file_upload.html', {
            'title': document.title,
            'user': document.user,
            'document_url': f"{settings.DOMAIN}{document.file.url}" if document.file else None
        })

        # Prepare the email
        email = EmailMultiAlternatives(subject, '', from_email, to_email)
        email.attach_alternative(html_content, "text/html")

        # Attach the file if it exists
        if document.file and os.path.exists(document.file.path):
            email.attach_file(document.file.path)
        else:
            logger.warning(f"File not found or does not exist: {document.file.path if document.file else 'No file'}")

        # Send the email
        email.send()
        print("Email sent with attachment!")

    except Document.DoesNotExist:
        logger.error(f"Document with ID {document_id} does not exist.")
    except Exception as e:
        logger.error(f"Error sending document upload email: {e}")
        print(f"Email error: {e}")