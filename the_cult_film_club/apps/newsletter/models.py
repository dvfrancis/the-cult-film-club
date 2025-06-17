from django.db import models
import uuid


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    genres = models.CharField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.email
