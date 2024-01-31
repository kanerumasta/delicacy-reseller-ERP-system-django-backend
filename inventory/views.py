
from datetime import date
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import *
from . serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Sum, F, Case, When
from django.db.models import fields, ExpressionWrapper
from .models import Delicacy
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser


class ItemView(APIView):
    
    def get(self, request, item_id = None):      
        if item_id:
            try:
                item = Item.objects.get(id = item_id)
                serializer = ItemSerializer(item)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Item.DoesNotExist:
                return Response({'error':'Item Does Not Exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Item.objects.select_related('variation__delicacy').order_by('variation__delicacy__name')
            serializer = ItemSerializer(items, many = True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        

    def post(self,request):
        
        try:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f'error: {e}')


class VariationView(APIView):
    def post(self, request):         
            serializer = VariationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, variation_id):
        variation = get_object_or_404(Variation, id = variation_id)
        serializer = VariationSerializer(variation,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

            

class DelicaciesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, delicacy_id = None):
        if delicacy_id:
            try:
                delicacy = Delicacy.objects.get(id = delicacy_id)
                serializer = DelicacySerializer(delicacy)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Delicacy.DoesNotExist:
                return Response({'error':'Delicacy Not Found'}, status = status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(f'unexpected error occured: {e}')
                return Response({'error': f'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                delicacies = Delicacy.objects.all()
                serializer = DelicacySerializer(delicacies, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Exception as e:
                print(f'error: {e}')
                return Response({'error':'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = DelicacySerializer(data = request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)

          

    def put(self, request, delicacy_id):
        try:
            delicacy = Delicacy.objects.get(id = delicacy_id)
            serializer = DelicacySerializer(delicacy, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
        except Delicacy.DoesNotExist:
            return Response({'error':'Delicacy Does Not Exist'}, status = status.HTTP_404_NOT_FOUND)
            

class InventoryView(APIView):

    def get(self,request, inventory_code=None):
        if inventory_code:
            try:
                inventory = get_object_or_404(Inventory, inventory_code = inventory_code)
                serializer = InventorySerializer(inventory)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail':'inventory not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                inventory = Inventory.objects.all().order_by('-arrival_date')
                serializer = InventorySerializer(inventory, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'detail', 'Error in fetching inventory'}, status = status.HTTP_404_NOT_FOUND)



    def post(self, request):
        data = request.data
        serializer = InventorySerializer(data = data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        print(serializer.errors)
        return Response({'detail':'Fail post inventory', 'status':400})

class SupplierView(APIView):
    def get(self, request, supplier_id = None):
        if supplier_id:
            pass
        else:
            try:
                suppliers = Supplier.objects.all()
                serializer = SupplierSerializer(suppliers, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except:
                return Response({'detail':'error fetching users'}, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        serializer = SupplierSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class CheckDelicacyNameView(APIView):
    def get(self, request):
        delicacy_name = request.GET.get('name', '')

        if not delicacy_name:
            return Response({'exists': False}, status=status.HTTP_400_BAD_REQUEST)

        delicacy_exists = Delicacy.objects.filter(name=delicacy_name).exists()

        return Response({'exists': delicacy_exists}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_total_low_stock_items(request):
    try:
        # Calculate the total low stock items across all delicacies
        total_low_stock = Delicacy.objects.annotate(
            low_stock_count=Sum(
                Case(
                    When(
                        variations__item__quantity__gt=0,
                        variations__item__quantity__lt=F('variations__item__reorder_level'),
                        then=1,
                    ),
                    default=0,
                    output_field=fields.IntegerField(),
                )
            )
        ).aggregate(total_low_stock=Sum('low_stock_count'))['total_low_stock']

        return Response({'total_low_stock': total_low_stock}, status=status.HTTP_200_OK)
    except Delicacy.DoesNotExist:
        return Response({'error': 'Delicacy not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_total_out_of_stock_items(request):
    try:
        
        total_out_of_stock = Delicacy.objects.annotate(
            out_of_stock_count=Sum(
                Case(
                    When(
                        variations__item__quantity=0,
                        then=1,
                    ),
                    default=0,
                    output_field=fields.IntegerField(),
                )
            )
        ).aggregate(total_out_of_stock=Sum('out_of_stock_count'))['total_out_of_stock']

        return Response({'total_out_of_stock': total_out_of_stock}, status=status.HTTP_200_OK)
    except Delicacy.DoesNotExist:
        return Response({'error': 'Delicacy not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_out_of_stock_items(request):
    try:
        # Retrieve all out-of-stock items
        out_of_stock_items = Delicacy.objects.filter(
            variations__item__quantity=0
        ).values(
            'id',
            'name',
            'variations__id',
            'variations__name',
            'variations__price',
            'variations__item__quantity',
        )

        # Organize the data into a dictionary for easy rendering in the frontend
        result = []
        for item in out_of_stock_items:
            result.append({
                'delicacy_id': item['id'],
                'delicacy_name': item['name'],   
                'variation_id': item['variations__id'],
                'variation_name': item['variations__name'],
                'variation_price': item['variations__price'],
                'quantity': item['variations__item__quantity'],
            })

        return Response(result, status=status.HTTP_200_OK)
    except Delicacy.DoesNotExist:
        return Response({'error': 'Delicacy not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_low_stock_items(request):
    try:
        low_stock_variations = Variation.objects.annotate(
        total_quantity=F('items__quantity'),
        low_stock=ExpressionWrapper(F('reorder_level') - F('items__quantity'), output_field=models.IntegerField()),
        ).filter(is_active=True,low_stock__gt=0)
        low_stock_variations_data = list(low_stock_variations.values())

        return Response({'low_stock_variations': low_stock_variations_data}, status=status.HTTP_200_OK)
    except:
        print('error')

    
@api_view(['GET'])
def get_expired_items(request):
    try:
        # Retrieve all expired items
        expired_items = Item.objects.filter(expiry_date__lt=date.today())

       
        result = []
        for item in expired_items:
            result.append({
                'inventory':item.inventory.id,
                'item_id': item.id,
                'variation_name': item.variation.name,
                'delicacy_name': item.variation.delicacy.name,
                'expiry_date': item.expiry_date,
              
            })

        return Response(result, status=status.HTTP_200_OK)
    except Item.DoesNotExist:
        return Response({'detail;': 'no expired items'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_delicacy_name(request, delicacy_id):
    try:
        delicacy = get_object_or_404(Delicacy, id = delicacy_id)
        if delicacy:
            return Response({'name': delicacy.name}, status=status.HTTP_200_OK)
        return Response({'name':'none'}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'detail':'error getting delicacy'})