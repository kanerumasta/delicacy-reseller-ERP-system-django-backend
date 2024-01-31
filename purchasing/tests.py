from django.test import TestCase
from django.utils import timezone
from inventory.models import *
from . models import PurchaseOrder, PurchaseOrderItem

class PurchaseOrderTestCase(TestCase):

    def setUp(self):
        # Create a sample supplier
        self.supplier = Supplier.objects.create(name='Sample Supplier', contact = "93450345", address = "sample address")

        # Create a sample variation
        self.delicacy = Delicacy.objects.create(name= 'delca', description = "this is the descript", image_url = "url")
        self.variation = Variation.objects.create(delicacy = self.delicacy, name='Sample Variation', price = 23.22)

    def test_purchase_order_creation(self):
        # Create a purchase order
        purchase_order = PurchaseOrder.objects.create(supplier=self.supplier)

        # Check if the purchase order code is generated
        self.assertIsNotNone(purchase_order.purchase_order_code)
        print(purchase_order.purchase_order_code)

        # Check if the purchase order is not received initially
        self.assertFalse(purchase_order.is_recieved)

        # Receive the order and check if the attributes are updated
        purchase_order.recieve_order()
        self.assertTrue(purchase_order.is_recieved)
        self.assertIsNotNone(purchase_order.recieved_at)

    def test_purchase_order_item_creation(self):
        # Create a purchase order
        purchase_order = PurchaseOrder.objects.create(supplier=self.supplier)

        # Create a purchase order item
        purchase_order_item = PurchaseOrderItem.objects.create(
            purchase_order=purchase_order,
            variation=self.variation,
            quantity_ordered=5
        )

        # Check if the string representation is correct
        self.assertEqual(
            str(purchase_order_item),
            f'Purchase Order Item - {self.variation}-{purchase_order}'
        )

        # Check if the quantity received can be updated
        purchase_order_item.quantity_received = 3
        purchase_order_item.save()
        self.assertEqual(purchase_order_item.quantity_received, 3)

# Note: Replace 'your_app' with the actual name of the app containing your models
