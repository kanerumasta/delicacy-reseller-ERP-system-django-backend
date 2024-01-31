from django.test import TestCase
from django.utils import timezone
from .models import Category, Delicacy, Variation, Supplier, Item

class InventoryModelTestCase(TestCase):
    def setUp(self):
        # Create test data for models
        self.category = Category.objects.create(name='Test Category')
        self.delicacy = Delicacy.objects.create(name='Test Delicacy', description='Test Description', image_url='test.jpg')
        self.variation = Variation.objects.create(name='Test Variation', delicacy=self.delicacy, price=10.99)
        self.supplier = Supplier.objects.create(name='Test Supplier', contact='Test Contact', address='Test Address')
        self.item = Item.objects.create(variation=self.variation, supplier=self.supplier, quantity=10,
                                       reorder_level=5, expiry_date=timezone.now(), arrival_date=timezone.now())

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'category - Test Category')

    def test_delicacy_str_method(self):
        self.assertEqual(str(self.delicacy), 'delicacy - Test Delicacy')

    def test_variation_str_method(self):
        self.assertEqual(str(self.variation), 'variation - Test Variation of Test Delicacy')

    def test_supplier_str_method(self):
        self.assertEqual(str(self.supplier), 'supplier - Test Supplier')

    def test_item_str_method(self):
        self.assertEqual(str(self.item), f'inventory item {self.variation.delicacy} in variation {self.variation}')

    def test_item_quantity_default(self):
        # Test that the default quantity for an item is set correctly
        new_variation = Variation.objects.create(name='New Variation', delicacy=self.delicacy, price=15.99)
        new_supplier = Supplier.objects.create(name='New Supplier', contact='New Contact', address='New Address')
        new_item = Item.objects.create(variation=new_variation, supplier=new_supplier, expiry_date=timezone.now(),
                                       arrival_date=timezone.now())
        self.assertEqual(new_item.quantity, 0)

 

    def test_item_arrival_in_past(self):
        # Test that arrival date is set in the past
        self.assertTrue(self.item.arrival_date < timezone.now())
