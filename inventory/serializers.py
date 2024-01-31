from .models import *
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework import serializers

    # name = models.CharField(max_length = 50, unique = True)
    # description = models.CharField(max_length=50)
    # image_url = models.CharField(max_length=255)



class VariationSerializer(ModelSerializer):

    class Meta:
        model = Variation
        fields = '__all__'

class DelicacySerializer(ModelSerializer):
    variations = VariationSerializer(many = True, read_only = True)
    class Meta:
        model = Delicacy
        fields = ['id','name','description','image','variations']
 

class SupplierSerializer(ModelSerializer):
    class Meta :
        model = Supplier
        fields = '__all__'



class ItemSerializer(ModelSerializer):
    # variation = VariationSerializer(read_only = True)
    class Meta:
        model = Item
        fields = '__all__'

    def to_representation(self, instance):
        # If the 'variation' field is present in the instance, include its serialized representation
        self.fields['variation'] = VariationSerializer()
        self.fields['supplier'] = SupplierSerializer()
        return super().to_representation(instance)


class InventorySerializer(ModelSerializer):
    
    inventory_items = ItemSerializer(many=True, read_only = True)
    class Meta:
        model = Inventory
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['supplier'] = SupplierSerializer()
        return super().to_representation(instance)