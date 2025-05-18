from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    photograph = CloudinaryField(
        'image',
        default='placeholder',
        blank=True,
        null=False
    )
    address = models.ForeignKey(
        'Address',
        on_delete=models.CASCADE,
        related_name="profile",
        blank=False,
        null=False)
    loyalty_points = models.IntegerField(
        default=0,
        blank=False,
        null=False
    )

    def clean(self):
        if (not self.location):
            raise ValidationError(
                "Please enter your location"
            )

    def __str__(self):
        return (
            f"This is {self.user.username}'s profile"
            if self.user
            else "This profile has no user"
        )


class Address(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="address"
    )
    first_line = models.CharField(max_length=100, blank=False, null=False)
    second_line = models.CharField(max_length=100, blank=True, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    county = models.CharField(max_length=50, blank=False, null=False)
    postcode = models.CharField(max_length=10, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    default_address = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"This is {self.user.username}'s address"


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    title = models.OneToOneField(
        'releases.Releases',
        on_delete=models.CASCADE,
        related_name="wishlists"
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )
    notes = models.TextField(
        max_length=1000,
        blank=True,
        null=False
    )
    priority = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        choices=[
            ('High', 'High'),
            ('Medium', 'Medium'),
            ('Low', 'Low')
        ],
        default='Medium'
    )
    quantity = models.IntegerField(
        default=1,
        blank=False,
        null=False
    )
    is_purchased = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )


def __str__(self):
    return f"This is {self.user.username}'s wishlist"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
