import logging 
import os 

import requests
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment 

logger = logging.getLogger(__name__)

def send_payment_to_monitoring_service(payment_id):
    try:
        print("reached here")
        payment = Payment.objects.select_related("merchant", "customer").get(pk=payment_id)

        payload = {
            "event_type": "payment.created",
            "transaction_id": str(payment.transaction_id),
            "amount": str(payment.amount),
            "currency": payment.currency,
            "status": payment.status,
            "customer_id": str(payment.customer.id),
            "merchant_id": str(payment.merchant.id),
            "created_at": payment.created_at.isoformat(),
        }
        print(payload)
        response = requests.post(
            os.environ.get("MONITORING_API_URL"),
            json=payload,
            headers={"x-monitoring-key": os.environ.get("MONITORING_API_KEY")},
            timeout=2,
        )
        response.raise_for_status()
    except Exception:
        # The payment is already committed. Monitoring failures
        # should not turn a successful payment creation into an API error.
        logger.exception(
            "Failed to send monitoring event for payment %s",
            payment_id,
        )

@receiver(post_save, sender=Payment)
def payment_created(sender, instance, created, **kwargs):
    if not created:
        return 
    transaction.on_commit(lambda: send_payment_to_monitoring_service(instance.id))