from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import UniqueConstraint
from django_ckeditor_5.fields import CKEditor5Field
from django_countries.fields import CountryField


class Profile(models.Model):
    """
    Stores user profile information, including photograph and addresses
    """
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
    # Note: This ManyToMany is likely redundant since Address has a FK to User.
    address = models.ManyToManyField(
        'Address',
        related_name="profile"
    )

    def __str__(self):
        return (
            f"This is {self.user.username}'s profile"
            if self.user
            else "No user assigned to this profile"
        )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Address(models.Model):
    """
    Stores a user's address details
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="address"
    )
    first_line = models.CharField(max_length=100)
    second_line = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    county = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=10)
    country = CountryField()
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    default_address = models.BooleanField(
        default=False,
        blank=True,
        null=False
    )
    label = models.CharField(
        max_length=15,
        blank=False,
        help_text="For example, 'Home' or 'Work'"
    )

    def save(self, *args, **kwargs):
        """
        Ensure only one default address per user
        """
        if self.default_address:
            Address.objects.filter(
                user=self.user,
                default_address=True
            ).exclude(pk=self.pk).update(default_address=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"This is {self.user.username}'s address"

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class PriorityLevel(models.TextChoices):
    HIGH = "High", "High"
    MEDIUM = "Medium", "Medium"
    LOW = "Low", "Low"


class Wishlist(models.Model):
    """
    Stores a user's wishlist of releases
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )
    title = models.ManyToManyField(
        'releases.Releases',
        through='WishlistItem',
        related_name="wishlists"
    )

    def __str__(self):
        return f"This is {self.user.username}'s wishlist"

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        constraints = [
            UniqueConstraint(fields=['user'], name='unique_user_wishlist')
        ]


class WishlistItem(models.Model):
    """
    Represents an item in a user's wishlist, with notes and priority
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    title = models.ForeignKey('releases.Releases', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    notes = CKEditor5Field(max_length=1000, blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices=PriorityLevel.choices,
        default=PriorityLevel.MEDIUM
    )
    is_purchased = models.BooleanField(default=False, verbose_name="Purchased")

    def __str__(self):
        return f"{self.title} in {self.wishlist} (Priority: {self.priority})"

    class Meta:
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update a Profile whenever a User is created or saved
    """
    Profile.objects.get_or_create(user=instance)
