from django.test import TestCase
from django.contrib.auth.models import User
from inventory.models import *
from .models import Requisition, RequisitionItem

class RequisitionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_requisition(self):
        requisition = Requisition.objects.create(
            requester=self.user,
            description='Test requisition',
            notes='Some notes',
        )
        self.assertEqual(requisition.approval_status, 'pending')
        self.assertIsNone(requisition.approver)
        self.assertIsNone(requisition.approved_at)

    def test_approve_requisition(self):
        requisition = Requisition.objects.create(requester=self.user, description='Test requisition')
        requisition.approve(approver_user=self.user, comment='Approved!')
        self.assertEqual(requisition.approval_status, 'approved')
        self.assertEqual(requisition.approver, self.user)
        self.assertIsNotNone(requisition.approved_at)

    def test_reject_requisition(self):
        requisition = Requisition.objects.create(requester=self.user, description='Test requisition')
        requisition.reject(approver_user=self.user, comment='Rejected!')
        self.assertEqual(requisition.approval_status, 'rejected')
        self.assertEqual(requisition.approver, self.user)
        self.assertIsNotNone(requisition.approved_at)

    def test_generate_requisition_code(self):
        requisition = Requisition.objects.create(requester=self.user, description='Test requisition')
        self.assertTrue(requisition.requisition_code.startswith('REQ'))

    def test_create_requisition_item(self):
        requisition = Requisition.objects.create(requester=self.user, description='Test requisition')
        delicacy = Delicacy.objects.create(name = "ampa", description = "wa ragud", image_url = "http:dfldfsodf")
        variation = Variation.objects.create(delicacy = delicacy,name='Test Variation', price=10.0)
        requisition_item = RequisitionItem.objects.create(requisition=requisition, variation=variation, quantity=2)
        self.assertEqual(requisition_item.requisition, requisition)
        self.assertEqual(requisition_item.variation, variation)
        self.assertEqual(requisition_item.quantity, 2)

