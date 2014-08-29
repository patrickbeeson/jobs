from __future__ import absolute_import

from django.core.mail import send_mail
from django.db.models.signals import post_save

from .models import Application


def send_confirmation(sender, instance, created, **kwargs):
    """
    Send a notification to the applicant letting them know their application has been received.
    """
    if instance.email_address:
        message = "Thank you for applying to The Variable." + '\n' + '\n' + "Due to the high volume of responses, we will only be able to contact you if we move forward with your candidacy."
        subject = "Your application has been received"
        send_mail(subject, message, 'noreply@mail.thevariable.com', [instance.email_address, ], fail_silently=False)
    else:
        pass

post_save.connect(send_confirmation, sender=Application)
