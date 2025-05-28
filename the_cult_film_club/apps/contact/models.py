from django.db import models
from django.core.validators import validate_email
from django_ckeditor_5.fields import CKEditor5Field


class ContactUs(models.Model):
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(
        validators=[validate_email],
        blank=False,
        null=False
    )
    message = CKEditor5Field(max_length=1000, blank=True, null=False)

    def __str__(self):
        return (
            f"This message was submitted by {self.first_name} {self.last_name}"
        )
