from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from . models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from rest_framework.decorators import api_view

class UserListView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    
class RegisterView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        data = request.data
        print(data)
        serializer = RegisterSerializer(data = data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status = status.HTTP_204_NO_CONTENT)
        

class AcceptUserView(APIView):
    # permission_classes = IsAdminUser
    def patch(self, request, user_id):
        user = get_object_or_404(User, id = user_id)

        if user.is_active:
            return Response({'detail':'User is already active'},status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({'detail':'Approving user is successful!'},status=status.HTTP_200_OK)

@api_view(['PATCH'])
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return Response({'detail':'success'}, status = status.HTTP_200_OK)


@api_view(['GET'])
def get_new_users(request):
    new_users = User.objects.filter(is_new = True).order_by('-date_joined')
    serializer = UserSerializer(new_users, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)