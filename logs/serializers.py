from rest_framework.serializers import ModelSerializer
from .models import TransactionLog
from authentication.serializers import UserSerializer
class LogSerializer(ModelSerializer):
	class Meta:
		model  = TransactionLog
		fields = '__all__'

	def to_representation(self, instance):
		self.fields['user'] = UserSerializer()
		return super().to_representation(instance)