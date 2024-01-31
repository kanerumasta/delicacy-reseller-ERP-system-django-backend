from django.db import models

import random


class Delicacy(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to = 'images/', null = True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'delicacy - {self.name}'


class Variation(models.Model):
    name = models.CharField(max_length= 255)
    delicacy = models.ForeignKey(Delicacy, on_delete=models.CASCADE, related_name="variations")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    reorder_level = models.PositiveIntegerField(null=True, blank = True)

    def __str__(self):
        return f'variation - {self.name} of {self.delicacy.name}'
    
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'supplier - {self.name}'



class Inventory(models.Model):
    UNIQUE_CODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    inventory_code = models.CharField(max_length=50, unique=True, blank = True, null = True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True, blank=True)
   
    arrival_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Inventory - {self.inventory_code}'
    
    def save(self, *args, **kwargs):
        print(self.inventory_code)
        if not self.inventory_code:
            self.inventory_code = self.generate_inventory_code()
            print(self.inventory_code)
            super().save(*args,**kwargs)

    def generate_inventory_code(self):
            return 'INV-' + ''.join(random.choice(self.UNIQUE_CODE_CHARS) for _ in range(6))
    


class Item(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name = 'inventory_items')
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name="items")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name = "items", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    expiry_date = models.DateField(null=True, blank = True)
    

    def delicacy(self):
        return self.variation.delicacy

    def __str__(self):
        return f'inventory item {self.variation.delicacy} in variation {self.variation}'
