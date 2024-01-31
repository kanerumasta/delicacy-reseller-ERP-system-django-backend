from django.db import models
from authentication.models import User
from inventory.models import Variation
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Requisition(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved','Approved'),
        ('rejected', 'Rejected'),
        ('ordered', 'Ordered'),

    ]

    requisition_code = models.CharField(unique=True, max_length=50, null = False, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_requisitions')
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default = 'pending')
    approver = models.ForeignKey(User, null=True, blank= True, on_delete=models.SET_NULL, related_name='approved_requisitions')
    description = models.TextField(null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    approval_comment = models.TextField(null = True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.requisition_code:
            self.requisition_code = self.generate_requisition_code()
        super().save(*args, **kwargs)

    def generate_requisition_code(self):
        timestamp_str = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex)[:6]
        return f'REQ-{timestamp_str}-{unique_id}'

    
    def approve(self, approver_user, comment = ''):
        if self.approval_status == 'pending':
            self.approval_status = 'approved'
            self.approver = approver_user
            self.approval_comment = comment
            self.approved_at = timezone.now()
            self.save()

    def reject(self, approver_user, comment = ''):
        if self.approval_status == 'pending':
            self.approval_status = 'rejected'
            self.approver = approver_user
            self.approval_comment = comment
            self.approved_at = timezone.now()
            self.save()

    def __str__(self):
        return f'Requisition - {self.requisition_code}'

@receiver(pre_save, sender=Requisition)
def pre_save_requisition(sender, instance, **kwargs):
    if not instance.requisition_code:
        instance.requisition_code = instance.generate_requisition_code()




class RequisitionItem(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='requisition_items')
    variation = models.ForeignKey(Variation,on_delete=models.CASCADE, blank=False)
    quantity = models.PositiveIntegerField(default=1,validators= [MinValueValidator(1)])

    def __str__(self):
        return f'Requisition Item - {self.variation}'


