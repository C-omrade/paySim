import uuid

from django.db import models
from merchant.models import Merchant
from customer.models import Customer
# Create your models here.

class Payment(models.Model):
    transaction_id = models.CharField(default=uuid.uuid4,max_length=100, unique=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"