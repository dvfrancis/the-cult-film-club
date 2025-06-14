import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from the_cult_film_club.apps.releases.models import Releases
from django_countries.fields import CountryField
from django.utils import timezone


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        "the_cult_film_club_account.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(
        blank_label="Country *",
        null=False,
        blank=False
    )
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default='',
        unique=True
    )
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    discount_code = models.CharField(max_length=50, blank=True, null=True)

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update total each time a line item is added,
        accounting for delivery costs and discount.
        """
        self.subtotal = (
            self.lineitems.aggregate(
                Sum('lineitem_total')
            )['lineitem_total__sum'] or 0
        )
        if self.subtotal < settings.FREE_DELIVERY:
            self.delivery_cost = (
                self.subtotal * settings.DELIVERY_RATE / 100
            )
        else:
            self.delivery_cost = 0
        # Subtract discount from subtotal + delivery
        self.total = max(self.subtotal + self.delivery_cost - self.discount, 0)
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    release = models.ForeignKey(
        Releases,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.release.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.order.order_number}'


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent = models.PositiveIntegerField(
        help_text="Discount percent (For example, 10 for 10%)"
    )
    valid_from = models.DateField(help_text="Start date (DD-MM-YYYY)")
    valid_to = models.DateField(help_text="End date (DD-MM-YYYY)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.code} ({self.percent}% off, "
            f"{self.valid_from.strftime('%d-%m-%Y')} to "
            f"{self.valid_to.strftime('%d-%m-%Y')})"
        )

    def is_valid(self):
        today = timezone.now().date()
        return (
            self.is_active and
            self.valid_from <= today <= self.valid_to
        )
