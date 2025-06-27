from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_order_total_on_save(sender, instance, created, **kwargs):
    """
    Signal handler to update the related Order's total
    whenever an OrderLineItem is created or updated.
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the related Order's total
    whenever an OrderLineItem is deleted.
    """
    instance.order.update_total()
