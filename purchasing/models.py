from django.db import models
from inventory.models import *
import random
from django.utils import timezone

class PurchaseOrder(models.Model):
   
    UNIQUE_CODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null = True, blank=True)
    purchase_order_code = models.CharField(max_length=13, unique = True, blank = True, null = True)
    recieved_at = models.DateTimeField(null=True, blank=True)
   
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    stocked = models.BooleanField(default = False)


    def __str__(self):
        return f'Purchase Order - {self.purchase_order_code}'
    
    def save(self, *args, **kwargs):
        print(self.status)
        if not self.purchase_order_code:
            self.purchase_order_code = self.generate_order_code()
        super().save(*args,**kwargs)


    def generate_order_code(self):
            return 'PO-' + ''.join(random.choice(self.UNIQUE_CODE_CHARS) for _ in range(7))
    
    def receive_order(self):
        self.status = "received"
        self.recieved_at = timezone.now()
        self.save()


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField(default=1)
    quantity_received = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'Purchase Order Item - {self.variation}-{self.purchase_order}'

