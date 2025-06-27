from django.db import models
from django.core.validators import validate_email
from django_ckeditor_5.fields import CKEditor5Field


class ContactUs(models.Model):
    """
    Model to store messages submitted via the Contact Us form.
    """

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created']  # Show newest messages first by default

    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the message was created"
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text="First name of the sender"
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text="Last name of the sender"
    )
    email = models.EmailField(
        validators=[validate_email],
        blank=False,
        null=False,
        help_text="Email address of the sender"
    )
    message = CKEditor5Field(
        max_length=1000,
        blank=False,
        null=False,
        help_text="Message content"
    )

    def __str__(self):
        return f"Message submitted by {self.first_name} {self.last_name}"
