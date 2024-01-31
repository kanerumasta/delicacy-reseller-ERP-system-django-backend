
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from . models import *
from . serializers import *
from inventory.models import *
from django.db import IntegrityError
from logs.utils import log_transaction

@api_view(['GET'])
def get_my_requisitions(request):
    try:
        requisitions = Requisition.objects.filter(requester=request.user.id)
        if requisitions.exists():  # Check if the queryset is not empty
            serializer = RequisitionSerializer(requisitions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No requisitions found for the user.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'detail': 'Error getting requisitions. {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class RequisitionView(APIView):
    def get(self, request, requisition_id=None):
        if requisition_id:
            try:
                requisition = Requisition.objects.get(id = requisition_id)
                serializer = RequisitionSerializer(requisition)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Requisition.DoesNotExist:
                return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
        else:
            requisitions = Requisition.objects.all().order_by('-created_at')
            serializer = RequisitionSerializer(requisitions, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            requester = request.user
            serializer = RequisitionSerializer(data = request.data)
            
            if serializer.is_valid():
                serializer.validated_data['requester'] = requester
                serializer.save()
                user = serializer.validated_data['requester']
                action = 'Created a new requisition'
                details = f"{user} - {action} - ref : {serializer.data['requisition_code']}"
                log_transaction(user, action, details)
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            print(e)
    def delete(self, request, requisition_id):
        try:
            requisition = get_object_or_404(Requisition, id = requisition_id)

            requisition.delete()
            return Response({'detail':'deleted'}, status = status.HTTP_200_OK)
        except Exception as e:
            raise e

class RequisitionItemView(APIView):
    def get(self, request, requisition_id = None):
        if requisition_id:
            print('requisition_id',requisition_id)
            try:
                requisition = get_object_or_404(Requisition, id=requisition_id)
                
                serializer = RequisitionSerializer(requisition)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except Requisition.DoesNotExist:
                return Response({'error':'Items does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                requisitions = Requisition.objects.all().order_by('-created_at')
                serializer = RequisitionSerializer(requisitions, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except:
                return Response({'error':'Error getting requisitions'}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request):
        serializer = RequisitionItemSerializer(data = request.data)
        for key, value in request.data.items():
            print(key, value)
        if serializer.is_valid():
            print('VALIDATED DATA')
            for key, value in serializer.validated_data.items():
                print(key, value)
            print(serializer.validated_data['variation'])
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            print('INVALID SERIALIZER DATA')
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class UserRequisitionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Filter requisitions based on the requester (user)
            requisitions = Requisition.objects.filter(requester=request.user).order_by('-created_at')

            if requisitions.exists():
                serializer = RequisitionSerializer(requisitions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'No requisitions found for the user.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail': f'Error getting requisitions. {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    
class ApproveRequisitionView(APIView):
    
    def patch(self, request, requisition_id):
        
        comment = request.data.get('comment')
        try:
            requisition = Requisition.objects.get(id = requisition_id)
        except Requisition.DoesNotExist:
            return Response({'detail':'Error in getting requisition'}, status = status.HTTP_400_BAD_REQUEST)

        if requisition.approval_status == 'pending':
            requisition.approve(request.user, comment)
            user = request.user
            action = 'has approved requisition'
            details = f"{user} {action} - RequisitionCode : {requisition.requisition_code}"
            log_transaction(user = user, action = action, details = details)
            return Response({'detail':'requisition is now approved'}, status = status.HTTP_200_OK)
        else:
            return Response({'detail':requisition.approval_status}, status = status.HTTP_400_BAD_REQUEST)
    

class RejectRequisitionView(APIView):
    def patch(self, request, requisition_id):
        comment = request.data.get('comment')
        try:
            requisition = Requisition.objects.get(id = requisition_id)
        except Requisition.DoesNotExist:
            return Response({'detail':'Error in getting requisition'}, status = status.HTTP_400_BAD_REQUEST)

        if requisition.approval_status == 'pending':
            requisition.reject(request.user, comment)
            user = request.user
            action = 'has rejected requisition'
            details = f"{user} {action} - RequisitionCode : {requisition.requisition_code}"
            log_transaction(user = user, action = action, details = details)
            return Response({'detail':'rejected requisition'}, status = status.HTTP_200_OK)
        else:
            return Response({'detail':requisition.approval_status}, status = status.HTTP_400_BAD_REQUEST)

            
@api_view(['PATCH'])
def create_order(request, requisition_id):
    requisition = get_object_or_404(Requisition, id = requisition_id)
    if requisition:
        requisition.approval_status = 'ordered'
        requisition.save()
        user = request.user
        action = 'has created a new order'
        details = f"{user} {action} for requisition : {requisition.requisition_code} by {requisition.requester}"
        log_transaction(user = user, action = action, details = details)
        return Response({'detail':'successfully ordered requisition'}, status = status.HTTP_200_OK)
    return Response({'detail':'failed', 'status':400})