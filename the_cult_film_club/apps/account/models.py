from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum


class Profile(models.Model):
    class Meta:
        verbose_name_plural = "Profiles"
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
    address = models.ManyToManyField(
        'Address',
        related_name="profile")
    loyalty_points = models.IntegerField(
        default=0,
        null=False
    )

    def __str__(self):
        return (
            f"This is {self.user.username}'s profile"
            if self.user
            else "No user assigned to this profile"
        )


class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="address"
    )
    first_line = models.CharField(max_length=100, blank=False, null=False)
    second_line = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=False, null=False)
    county = models.CharField(max_length=50, blank=False, null=False)
    postcode = models.CharField(max_length=10, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    default_address = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    def save(self, *args, **kwargs):
        if self.default_address:
            # Set all other addresses for this user to default_address=False
            Address.objects.filter(
                user=self.user,
                default_address=True
            ).exclude(pk=self.pk).update(default_address=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"This is {self.user.username}'s address"


class PriorityLevel(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Wishlist(models.Model):
    class Meta:
        verbose_name_plural = "Wishlists"
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )
    title = models.ManyToManyField(
        'releases.Releases',
        related_name="wishlists"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.value) for tag in PriorityLevel],
        default=PriorityLevel.MEDIUM.value
    )
    quantity = models.IntegerField(default=1)
    is_purchased = models.BooleanField(default=False, verbose_name="Purchased")

    def __str__(self):
        return f"This is {self.user.username}'s wishlist"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)
