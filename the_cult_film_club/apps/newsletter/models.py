from django.db import models
import uuid


class NewsletterSignup(models.Model):
    """
    Stores newsletter subscriber details such as
    email, optional genre preferences, and an unsubscribe token.
    """
    email = models.EmailField(
        unique=True,
        help_text="Subscriber's email address"
    )
    genres = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated list of preferred genres"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the subscription was created"
    )
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Token used to securely unsubscribe via email link"
    )

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
        ordering = ['-date_joined']  # Most recent signups first

    def __str__(self):
        return self.email
