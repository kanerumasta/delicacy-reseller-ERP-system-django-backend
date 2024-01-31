from rest_framework.serializers import ModelSerializer
from . models import *
from inventory.serializers import VariationSerializer
from authentication.serializers import UserSerializer
from rest_framework import serializers

class RequisitionItemSerializer(ModelSerializer):
    # variation = VariationSerializer(read_only = True)
    class Meta:
        model = RequisitionItem
        fields = '__all__'

    def to_representation(self, instance):
        # If the 'variation' field is present in the instance, include its serialized representation
        self.fields['variation'] = VariationSerializer()
       
        return super().to_representation(instance)



class RequisitionSerializer(ModelSerializer):
    requester = UserSerializer(read_only = True)
    requisition_items = RequisitionItemSerializer(many=True, read_only = True)
    class Meta:
        model = Requisition
        fields = ['id','requisition_code','created_at','requester','approval_status','approver','description','notes','approval_comment','approved_at','requisition_items']
