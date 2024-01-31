from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework  import status
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

class PurchaseOrderView(APIView):
    def get(self,request, purchase_order_code = None):
        if purchase_order_code:
            try:
                purchase_order = PurchaseOrder.objects.get(purchase_order_code = purchase_order_code)
                serializer = PurchaseOrderSerializer(purchase_order)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except PurchaseOrder.DoesNotExist:
                return Response({'detail':'Purchase Order Does Not Exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                purchase_orders = PurchaseOrder.objects.all().order_by('-created_at')
                serializer = PurchaseOrderSerializer(purchase_orders, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except:
                return Response({'detail':'Error in getting purchase orders'}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = PurchaseOrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            user = request.user
            action = 'has created purchase order'
            details = f"{user} {action} {serializer.data['purchase_order_code']}"
            log_transaction(user = user, action = action, details = details)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PurchaseOrderItemView(APIView):
         
    def post(self, request, *args, **kwargs):
        serializer = PurchaseOrderItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status = status.HTTP_201_CREATED)


@api_view(['PATCH'])
def received_order(request, order_code):
    try:
        order = get_object_or_404(PurchaseOrder, purchase_order_code = order_code)
        order.receive_order()
        user = request.user
        action = 'received order'
        details = f"{user} {action} po_code: {order_code}"
        log_transaction(user = user, action = action, details = details)
        return Response({'detail':'success', 'status':200})
    except Exception as e:
        return Response({'detail':'error', 'status':400})

@api_view(['PATCH'])
def add_to_inventory(request, order_code):
    try:
        order = get_object_or_404(PurchaseOrder, purchase_order_code = order_code)
        order.status = "added"
        order.save()
        user = request.user
        action = 'has added purchase order'
        details = f"{user} {action} {order_code} to inventory"
        log_transaction(user = user, action = action, details = details)
        return Response({'detail':'added to inventory'}, status = status.HTTP_200_OK)
    except :
        return Response({'detail':'error'}, status = status.HTTP_400_BAD_REQUEST)


