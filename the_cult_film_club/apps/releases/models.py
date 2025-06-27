from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django_ckeditor_5.fields import CKEditor5Field


class Releases(models.Model):
    class Meta:
        verbose_name = "Release"
        verbose_name_plural = "Releases"
    title = models.CharField(max_length=100, blank=False, null=False)
    release_date = models.DateField(blank=False, null=False)
    director = models.CharField(max_length=100, blank=True, null=True)
    description = CKEditor5Field(max_length=1000, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    subgenre = models.CharField(max_length=50, blank=True, null=True)
    resolution = models.CharField(max_length=10, blank=True, null=True)
    special_features = CKEditor5Field(max_length=2000, blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    censor_status = models.CharField(max_length=500, blank=True, null=True)
    packaging = models.CharField(max_length=500, blank=True, null=True)
    copies_available = models.IntegerField(blank=False, null=False, default=0)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"{self.title}"

    @property
    def average_rating(self):
        return (
            Rating.objects
            .filter(title=self)
            .aggregate(avg=Avg('rating'))['avg']
        )

    @property
    def featured_image(self):
        return self.images.filter(is_featured=True).first()


class Rating(models.Model):
    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = (
            ('user', 'title'),
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    title = models.ForeignKey(
        'releases.Releases',
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=False,
        null=False
    )
    review = CKEditor5Field(max_length=1500, blank=True, null=True)
    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return (
            f"{self.user.username} rated "
            f"{self.title.title} as {self.rating}"
        )


class Images(models.Model):
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
    title = models.ForeignKey(
        'releases.Releases',
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = CloudinaryField(
        'image',
        default='holding_image',
        blank=True,
        null=False
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )
    is_featured = models.BooleanField(
        verbose_name="Featured Image",
        default=False,
        blank=False,
        null=False
    )

    def __str__(self):
        return f"Image for {self.title.title}"

    def save(self, *args, **kwargs):
        # If this image is being set as featured,
        # unset all others for this release
        if self.is_featured and self.title:
            Images.objects.filter(
                title=self.title,
                is_featured=True
            ).exclude(pk=self.pk).update(is_featured=False)
        # Assign image to release's ManyToManyField
        super().save(*args, **kwargs)
        if self.title:
            self.title.image.add(self)
