from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Donation


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        donation = get_object_or_404(Donation, donation_id=ipn.invoice)
        donation.status = 'completed'
        donation.save()
    