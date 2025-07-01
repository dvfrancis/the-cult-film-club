import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.db.models import Sum
from django.conf import settings
from the_cult_film_club.apps.releases.models import Releases
from django_countries.fields import CountryField
from django.utils import timezone


class Order(models.Model):
    """
    Represents a customer's order, including user profile (optional),
    shipping details, payment info, and totals.
    """
    order_number = models.CharField(
        max_length=32,
        null=False,
        editable=False,
        unique=True,
        help_text="Unique order identifier"
    )
    user_profile = models.ForeignKey(
        "the_cult_film_club_account.Profile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders',
        help_text="Profile of user who placed the order (optional)"
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
        max_digits=6, decimal_places=2, null=False, default=Decimal('0.00')
    )
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal('0.00')
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=Decimal('0.00')
    )
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default='',
        unique=True,
        help_text="Stripe Payment Intent ID"
    )
    discount = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('0.00'),
        help_text="Discount amount subtracted from total"
    )
    discount_code = models.CharField(
        max_length=50, blank=True, null=True,
        help_text="Code for applied discount (if any)"
    )

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID4.
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update subtotal, delivery cost, and total for the order.
        Called when line items are added/removed/updated.
        """
        self.subtotal = (
            self.lineitems.aggregate(
                Sum('lineitem_total')
            )['lineitem_total__sum'] or Decimal('0.00')
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if self.subtotal < settings.FREE_DELIVERY:
            self.delivery_cost = (
                self.subtotal * Decimal(settings.DELIVERY_RATE)
                / Decimal('100')
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            self.delivery_cost = Decimal('0.00')

        # Ensure total is never negative
        self.total = max(
            self.subtotal + self.delivery_cost - self.discount,
            Decimal('0.00')
        ).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        self.save()

    def save(self, *args, **kwargs):
        """
        Override save to generate order_number if not set.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return string representation of the order.
        """
        return f"Order {self.order_number}"


class OrderLineItem(models.Model):
    """
    Line item for a particular release within an order.
    Tracks quantity and total price for that item.
    """
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
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=1,
        help_text="Quantity of this release in the order"
    )
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False,
        help_text="Total price for this line item (price * quantity)"
    )

    def save(self, *args, **kwargs):
        """
        Calculate lineitem_total and update related order total on save.
        """
        self.lineitem_total = (self.release.price * self.quantity).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        super().save(*args, **kwargs)
        # Update order totals after saving the line item
        self.order.update_total()

    def __str__(self):
        """
        Return string representation of line item.
        """
        return (
            f'LineItem for Order {self.order.order_number} - '
            f'{self.release.title} x {self.quantity}'
        )


class DiscountCode(models.Model):
    """
    Represents a discount code with a percentage discount valid within
    a date range and can be active or inactive.
    """
    code = models.CharField(max_length=50, unique=True)
    percent = models.PositiveIntegerField(
        help_text="Discount percent (For example, 10 for 10%)"
    )
    valid_from = models.DateField(help_text="Start date (DD-MM-YYYY)")
    valid_to = models.DateField(help_text="End date (DD-MM-YYYY)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Return string representation of discount code and validity.
        """
        return (
            f"{self.code} ({self.percent}% off, "
            f"{self.valid_from.strftime('%d-%m-%Y')} to "
            f"{self.valid_to.strftime('%d-%m-%Y')})"
        )

    def is_valid(self):
        """
        Check if the discount code is currently valid.
        """
        today = timezone.now().date()
        return (
            self.is_active and
            self.valid_from <= today <= self.valid_to
        )
