from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from cloudinary.models import CloudinaryField


class Releases(models.Model):
    image = models.ForeignKey(
        'Images',
        on_delete=models.CASCADE,
        related_name="releases",
        blank=True,
        null=True
    )
    title = models.CharField(max_length=100, blank=False, null=False)
    release_date = models.DateField(blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    subgenre = models.CharField(max_length=50, blank=True, null=True)
    resolution = models.CharField(max_length=5, blank=True, null=True)
    special_features = models.TextField(max_length=2000, blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    censor_status = models.CharField(max_length=10, blank=True, null=True)
    copies_available = models.IntegerField(blank=True, null=True)
    packaging = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.release_date})"

    @property
    def average_rating(self):
        return (
            Rating.objects
            .filter(title__title=self.title)
            .aggregate(avg=Avg('rating'))['avg']
        )


class Rating(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="rating"
    )
    title = models.OneToOneField(
        'releases.Releases',
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.IntegerField(blank=False, null=False)
    review = models.TextField(max_length=1500, blank=True, null=True)
    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return (
            f"{self.user.username} rated "
            f"{self.release.title} as {self.rating}"
        )


class Images(models.Model):
    title = models.OneToOneField(
        'releases.Releases',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField(
        'image',
        default='placeholder',
        blank=True,
        null=False
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        null=False
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )
    is_featured = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"Image for {self.title.title}"
