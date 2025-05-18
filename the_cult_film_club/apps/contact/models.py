from django.db import models


class ContactUs(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return (
            f"This message was submitted by {self.first_name} {self.last_name}"
        )
