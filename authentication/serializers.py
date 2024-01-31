from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from . models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)  
        
        token['username'] = user.username
        token['is_admin'] = user.is_admin
        token['is_active'] = user.is_active
        return token
    
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        user = self.user
        # Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError("User account is not active.")
        return data



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())],
            },
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        

        


        
        user.set_password(validated_data['password'])
        user.save()

        return user
