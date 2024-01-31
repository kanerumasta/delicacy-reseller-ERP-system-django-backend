from rest_framework.serializers import ModelSerializer
from . models import *
from inventory.serializers import VariationSerializer


class PurchaseOrderItemSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['variation'] = VariationSerializer()
        return super().to_representation(instance)


class PurchaseOrderSerializer(ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, read_only = True)
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

